# jobs/management/commands/fetch_jobs.py
import requests
from django.core.management.base import BaseCommand
from jobs.models import Job

RAPIDAPI_KEY  = "d8101e5c1emsh0d830aa0dee6a1dp197228jsn24a5db2cf01d"
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"

QUERIES = [
    ("python developer",    "python"),
    ("java developer",      "java"),
    ("php developer",       "php"),
    ("react developer",     "react"),
    ("nodejs developer",    "node"),
    ("angular developer",   "angular"),
    ("machine learning",    "ml"),
    ("data scientist",      "data"),
    ("golang developer",    "golang"),
    ("devops engineer",     "devops"),
    ("flutter developer",   "flutter"),
    ("wordpress developer", "wordpress"),
    ("fullstack developer", "fullstack"),
    ("android developer",   "android"),
]


class Command(BaseCommand):
    help = "Fetch real jobs from JSearch API into your database"

    def add_arguments(self, parser):
        parser.add_argument("--query",    type=str, default="")
        parser.add_argument("--skill",    type=str, default="")
        parser.add_argument("--location", type=str, default="India")
        parser.add_argument("--count",    type=int, default=5)
        parser.add_argument("--all",      action="store_true")

    def fetch_jobs(self, query, skill, location, count):
        headers = {
            "X-RapidAPI-Key":  RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
        }
        params = {
            "query":     f"{query} in {location}",
            "num_pages": "1",
        }
        try:
            r = requests.get(
                "https://jsearch.p.rapidapi.com/search",
                headers=headers, params=params, timeout=15
            )
            data = r.json()
        except Exception as e:
            self.stderr.write(f"Error: {e}")
            return 0

        created = 0
        for job in data.get("data", [])[:count]:
            title      = (job.get("job_title")       or "").strip()
            company    = (job.get("employer_name")   or "").strip()
            loc        = (job.get("job_city") or job.get("job_country") or "Remote").strip()
            apply_link = (job.get("job_apply_link")  or "").strip()
            description= (job.get("job_description") or "")[:2000]
            emp_type   = (job.get("job_employment_type") or "").lower()

            if "intern" in emp_type:
                job_type = "intern"
            elif "part" in emp_type or "contract" in emp_type:
                job_type = "fresher"
            else:
                job_type = "fulltime"

            if not title or not company:
                continue

            obj, was_created = Job.objects.get_or_create(
                title=title,
                company=company,
                defaults={
                    "location":     loc,
                    "job_type":     job_type,
                    "skill":        skill,
                    "salary":       0,
                    "apply_link":   apply_link,
                    "description":  description,
                    "requirements": "",
                },
            )
            if was_created:
                created += 1
                self.stdout.write(f"  + [{skill}] {title} @ {company}")
            else:
                self.stdout.write(f"  = Exists: {title}")

        return created

    def handle(self, *args, **options):
        total    = 0
        location = options["location"]
        count    = options["count"]

        if options["all"]:
            self.stdout.write("\nFetching all skill categories...\n")
            for query, skill in QUERIES:
                self.stdout.write(f"\n--- {skill.upper()} ---")
                total += self.fetch_jobs(query, skill, location, count)

        elif options["query"] and options["skill"]:
            total += self.fetch_jobs(options["query"], options["skill"], location, count)

        else:
            self.stdout.write(
                "Usage:\n"
                "  python manage.py fetch_jobs --all\n"
                "  python manage.py fetch_jobs --all --count 10\n"
                "  python manage.py fetch_jobs --query 'react developer' --skill react\n"
            )
            return

        self.stdout.write(f"\nDone! {total} new jobs added.")
        self.stdout.write(f"Total in DB: {Job.objects.count()}\n")
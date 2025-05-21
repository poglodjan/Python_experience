from agents.workforce import JobSearchWorkforce

if __name__ == "__main__":
    workforce = JobSearchWorkforce()
    results = workforce.run()

    print("=== Found Job Positions ===")
    for job in results["job_positions"]:
        print(f"{job['title']} | {job['salary']} PLN | {job['location']} | {job['url']}")

    print("\n=== Learning Resources ===")
    for res in results["learning_resources"]:
        print(f"{res['title']} - {res['href']}")

    print("\n=== 2-Week Interview Preparation Plan ===")
    for day in results["interview_preparation_plan"]:
        print(f"Day {day['day']}: {day['goal']} - {day['resources']}")
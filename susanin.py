import server
import fixtures


def run_susanin():
    user_repo, area_repo, task_repo = fixtures.create_data()
    server.run(user_repo=user_repo, area_repo=area_repo, task_repo=task_repo)
    pass


if __name__ == "__main__":
    run_susanin()

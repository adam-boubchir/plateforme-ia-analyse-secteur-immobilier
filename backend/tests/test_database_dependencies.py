from app.dependencies.database import (
    get_immo_session,
    get_ministry_session,
)


def main():

    print("=" * 80)
    print("DATABASE DEPENDENCIES TEST")
    print("=" * 80)

    immo_db = get_immo_session()

    ministry_db = get_ministry_session()

    print()

    print("IMMO_AI session :", type(immo_db).__name__)

    print("Ministry session :", type(ministry_db).__name__)

    immo_db.close()

    ministry_db.close()

    print()

    print("✅ TEST PASSED")


if __name__ == "__main__":
    main()
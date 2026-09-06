import argparse

from api.auth import generate_api_key, hash_api_key
from api.db import init_db, register_device


def register(device_id, farm_id):
    api_key = generate_api_key()
    register_device(device_id, farm_id, hash_api_key(api_key))
    print(f"device_id: {device_id}")
    print(f"farm_id:   {farm_id}")
    print(f"api_key:   {api_key}")
    print("Store this key now — it is not recoverable, only re-issuable.")


def main():
    parser = argparse.ArgumentParser(description="Terrin device provisioning")
    sub = parser.add_subparsers(dest="command", required=True)

    register_cmd = sub.add_parser("register-device", help="Provision a new device or rotate its key")
    register_cmd.add_argument("device_id")
    register_cmd.add_argument("farm_id")

    args = parser.parse_args()
    init_db()

    if args.command == "register-device":
        register(args.device_id, args.farm_id)


if __name__ == "__main__":
    main()

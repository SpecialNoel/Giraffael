# one_click_tester.sh

# To run this script: ./one_click_tester.sh
# Run this command in case of permission denial: chmod +x one_click_tester.sh

docker compose down                    # Stops and delete current docker container instances
docker compose up --build -d           # Start and create docker container instances

sleep 3                                # Pause the script for a couple seconds

python3 -m client.src.app.client_chat  # Start client side operations

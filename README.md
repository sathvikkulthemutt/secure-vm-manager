# Secure VM Manager

Secure VM Manager is a lightweight virtualization platform that uses Docker containers to simulate virtual machines (VMs). It supports VM lifecycle management, snapshots, restoration, and stores metadata in SQLite. Perfect for learning container orchestration, cloud concepts, and DevOps basics.

---

## Setup and Run

Clone the repository, enter the folder, create a virtual environment, activate it, install dependencies, initialize the database, start Docker, and run the backend—all in order:

```bash
# 1. Clone the repository
git clone https://github.com/sathvikkulthemutt/secure-vm-manager.git
cd secure-vm-manager

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize the database
python3 -c "from models.db import Base, engine; from models.models import VM; Base.metadata.create_all(engine)"

# 5. Ensure Docker is running
docker ps

# 6. Run the Flask backend
python app.py

# 7. Example curl commands to test API
curl -X POST http://localhost:5001/vm/create -H "Content-Type: application/json" -d '{"name": "vm1", "image": "ubuntu:22.04"}'
curl -X POST http://localhost:5001/vm/snapshot -H "Content-Type: application/json" -d '{"name": "vm1", "snapshot_name": "vm1_snap1"}'
curl -X POST http://localhost:5001/vm/restore -H "Content-Type: application/json" -d '{"snapshot_name": "vm1_snap1", "new_vm_name": "vm1_restored"}'
curl http://localhost:5001/vm/list

# 8. Compare Original vs Restored VM
docker cp exited_vm:/ ./exited_vm_fs
docker cp restored_vm:/ ./restored_vm_fs
diff -r ./exited_vm_fs ./restored_vm_fs

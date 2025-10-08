import docker
from docker.errors import APIError, NotFound, ImageNotFound
from models.db import SessionLocal
from models.models import VM

client = docker.from_env()


def create_vm(name, image="ubuntu:22.04"):
    session = SessionLocal()
    try:
        # Check if container name already exists
        try:
            client.containers.get(name)
            return {"error": f"Container '{name}' already exists"}
        except NotFound:
            pass

        # Ensure image exists
        try:
            client.images.get(image)
        except ImageNotFound:
            client.images.pull(image)

        container = client.containers.run(image, name=name, detach=True, tty=True)
        vm = VM(name=name, image=image, status="running")
        session.add(vm)
        session.commit()
        return {"status": "success", "vm": name, "container_id": container.id[:12]}
    except APIError as e:
        return {"error": str(e)}
    finally:
        session.close()


def start_vm(name):
    session = SessionLocal()
    try:
        container = client.containers.get(name)
        container.start()
        _update_status(name, "running", session)
        return {"status": "started", "vm": name}
    except NotFound:
        return {"error": f"No container named '{name}'"}
    except APIError as e:
        return {"error": str(e)}
    finally:
        session.close()


def stop_vm(name):
    session = SessionLocal()
    try:
        container = client.containers.get(name)
        container.stop()
        _update_status(name, "stopped", session)
        return {"status": "stopped", "vm": name}
    except NotFound:
        return {"error": f"No container named '{name}'"}
    except APIError as e:
        return {"error": str(e)}
    finally:
        session.close()


def remove_vm(name):
    session = SessionLocal()
    try:
        container = client.containers.get(name)
        container.remove(force=True)
        vm = session.query(VM).filter_by(name=name).first()
        if vm:
            session.delete(vm)
            session.commit()
        return {"status": "deleted", "vm": name}
    except NotFound:
        return {"error": f"No container named '{name}'"}
    except APIError as e:
        return {"error": str(e)}
    finally:
        session.close()


def list_vms():
    try:
        containers = client.containers.list(all=True)
        return [
            {"name": c.name, "status": c.status, "id": c.id[:12]} for c in containers
        ]
    except APIError as e:
        return {"error": str(e)}


def snapshot_vm(name, snapshot_name):
    try:
        container = client.containers.get(name)
        image = container.commit(repository=snapshot_name)
        return {"status": "snapshot_created", "snapshot_name": snapshot_name, "image_id": image.id[:12]}
    except NotFound:
        return {"error": f"No container named '{name}'"}
    except APIError as e:
        return {"error": str(e)}


def restore_vm(snapshot_name, new_vm_name):
    session = SessionLocal()
    try:
        # Check if container already exists
        try:
            client.containers.get(new_vm_name)
            return {"error": f"Container '{new_vm_name}' already exists"}
        except NotFound:
            pass

        # Check if snapshot image exists
        try:
            client.images.get(snapshot_name)
        except ImageNotFound:
            return {"error": f"No snapshot image named '{snapshot_name}'"}

        container = client.containers.run(snapshot_name, name=new_vm_name, detach=True, tty=True)
        vm = VM(name=new_vm_name, image=snapshot_name, status="running")
        session.add(vm)
        session.commit()
        return {"status": "restored", "vm": new_vm_name, "container_id": container.id[:12]}
    except APIError as e:
        return {"error": str(e)}
    finally:
        session.close()


def _update_status(name, status, session):
    vm = session.query(VM).filter_by(name=name).first()
    if vm:
        vm.status = status
        session.commit()

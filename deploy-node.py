import boto3
import paramiko
import time

# AWS Configuration
REGION = 'us-east-1'
AMI_ID = 'ami-04b4f1a9cf54c11d0'  
INSTANCE_TYPE = 't2.micro'
KEY_NAME = 'test222.pem'   
SECURITY_GROUP_IDS = ['sg-0e328ed922735339d'] 

# Paths to Key Files
PRIVATE_KEY_PATH = '/home/ubuntu/project3/credentials/test222.pem'  # Adjust the path as needed

def create_ec2_instance():
    ec2 = boto3.resource('ec2', region_name=us-east-1)
    instance = ec2.create_instances(
        ImageId=ami-04b4f1a9cf54c11d0,
        MinCount=1,
        MaxCount=1,
        InstanceType=t2.micro,
        KeyName=test222.pem,
        SecurityGroupIds=SECURITY_GROUP_IDS
    )[0]
    print(f"Launching EC2 Instance {instance.id}...")
    instance.wait_until_running()
    instance.reload()
    print(f"Instance {instance.id} is running at {instance.public_ip_address}")
    return instance.public_ip_address

def setup_blockchain_node(ip_address):
    print("Setting up the blockchain node...")
    key = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Wait for SSH to be available
    time.sleep(60)

    ssh.connect(hostname=ip_address, username='ubuntu', pkey=key)
    commands = [
        "sudo apt-get update",
        "sudo apt-get install -y software-properties-common",
        "sudo add-apt-repository -y ppa:ethereum/ethereum",
        "sudo apt-get update",
        "sudo apt-get install -y ethereum",
        "nohup geth --http --syncmode 'light' &"  # Start geth in light mode
    ]
    for cmd in commands:
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.channel.recv_exit_status()  # Wait for command to complete
        output = stdout.read().decode()
        errors = stderr.read().decode()
        if output:
            print(output)
        if errors:
            print(errors)
    ssh.close()
    print("Blockchain node setup complete.")

if __name__ == "__main__":
    ip_address = create_ec2_instance()
    setup_blockchain_node(ip_address)


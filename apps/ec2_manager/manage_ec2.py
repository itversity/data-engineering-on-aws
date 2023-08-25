import boto3


def main():
    ec2 = boto3.resource('ec2')
    actions = ['start', 'stop', 'terminate']
    print('Please select an action: ')
    for idx, action in enumerate(actions):
        print(f"{idx + 1}. {action}")
    action = input("What do you want to do? (start/stop/terminate): ")
    instances = ec2.instances.all()
    for instance in instances:
        # Get name of each instance
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                name = tag['Value']
        print(f"{instance.id} - {name} - {instance.state['Name']}")


if __name__ == '__main__':
    main()
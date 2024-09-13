# Instructions on creating a new event bus from scratch.

Creating a new event bus in AWS EventBridge involves several steps. Here are detailed instructions to create and configure a new event bus from scratch using the AWS Management Console, AWS CLI, and AWS CloudFormation.

### 1. Using AWS Management Console

1. **Sign in to the AWS Management Console**:
   - Navigate to the [AWS Management Console](https://aws.amazon.com/console/).

2. **Open the Amazon EventBridge Console**:
   - In the search bar, type "EventBridge" and select "Amazon EventBridge".

3. **Create a New Event Bus**:
   - In the left-hand navigation pane, click on "Event buses".
   - Click the "Create event bus" button.
   - Enter a name for your new event bus (e.g., `MyCustomEventBus`).
   - Optionally, add a resource-based policy to grant permissions for other AWS accounts or services to put events on this event bus.
   - Click "Create".

4. **Verify Creation**:
   - Your new event bus should now be listed under the "Event buses" section.

### 2. Using AWS CLI

1. **Install and Configure AWS CLI**:
   - If you haven't installed the AWS CLI, follow the [installation guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
   - Configure the CLI with your credentials by running `aws configure`.

2. **Create a New Event Bus**:
   - Run the following command to create a new event bus:

     ```sh
     aws events create-event-bus --name MyCustomEventBus
     ```

3. **Verify Creation**:
   - List all event buses to verify the creation:

     ```sh
     aws events list-event-buses
     ```

### 3. Using AWS CloudFormation

1. **Create a CloudFormation Template**:
   - Create a file named `eventbus.yaml` with the following content:

     ```yaml
     AWSTemplateFormatVersion: '2010-09-09'
     Description: CloudFormation template to create a custom EventBridge event bus

     Resources:
       MyCustomEventBus:
         Type: AWS::Events::EventBus
         Properties:
           Name: MyCustomEventBus

     Outputs:
       EventBusName:
         Description: Name of the custom event bus
         Value: !Ref MyCustomEventBus
     ```

2. **Deploy the CloudFormation Stack**:
   - Run the following AWS CLI command to create the stack:

     ```sh
     aws cloudformation create-stack --stack-name MyEventBusStack --template-body file://eventbus.yaml
     ```

3. **Verify Creation**:
   - Once the stack creation is complete, verify the event bus in the EventBridge console or by listing event buses using the AWS CLI:

     ```sh
     aws events list-event-buses
     ```

### Summary

- **AWS Management Console**: Provides a user-friendly interface for creating and managing event buses.
- **AWS CLI**: Allows quick creation and management of event buses via command-line commands.
- **AWS CloudFormation**: Enables infrastructure as code, allowing for version-controlled and repeatable deployments.

By following these steps, you can create a new event bus in AWS EventBridge and start using it to manage events within your AWS environment.
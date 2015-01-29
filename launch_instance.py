from boto.ec2.connection import EC2Connection
from boto.ec2.blockdevicemapping import BlockDeviceType
from boto.ec2.blockdevicemapping import BlockDeviceMapping
import time

def launchBaseInstance(ami='your-default-ami'):
  '''Launch a single instance of the provided ami'''
  conn = EC2Connection()
  # Declare the block device mapping for ephemeral disks
  mapping = BlockDeviceMapping()
  eph0 = BlockDeviceType()
  eph1 = BlockDeviceType()
  eph0.ephemeral_name = 'ephemeral0'
  eph1.ephemeral_name = 'ephemeral1'
  mapping['/dev/sdb'] = eph0
  mapping['/dev/sdc'] = eph1
  # Now, ask for a reservation
  reservation = conn.run_instances(ami, instance_type='m1.large', key_name='ec2-keypair', placement='us-east-1a', block_device_map = mapping)
  # And assume that the instance we're talking about is the first in the list
  # This is not always a good assumption, and will likely depend on the specifics
  # of your launching situation. For launching an isolated instance while no
  # other actions are taking place, this is sufficient.
  instance = reservation.instances[0]
  print('Waiting for instance to start...')
  # Check up on its status every so often
  status = instance.update()
  while status == 'pending':
    time.sleep(10)
    status = instance.update()
  if status == 'running':
    print('New instance "' + instance.id + '" accessible at ' + instance.public_dns_name)
  else:
    print('Instance status: ' + status)
    return
  # If we got through the launching successfully, go ahead and create and attach a volume
  attachEBS(instance)
  # Now, bootstrap the deployment of this instance!
  with(settings(host_string=instance.public_dns_name)):
  # This is the fabric task for bootstrapping a running instance
  bootstrap()

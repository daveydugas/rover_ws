from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'rover_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
        (os.path.join("share", package_name,"rviz"), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='davey',
    maintainer_email='ddugashf1@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'send_service_call = rover_bringup.send_service_call:main',
            'demo_node = rover_bringup.demo_node:main',
            'send_motor_commands = rover_bringup.send_motor_commands:main',
            'dummy_publisher = rover_bringup.dummy_publisher:main',
            'take_me_home = rover_bringup.take_me_home:main'
        ],
    },
)

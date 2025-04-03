from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'rover_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join("share", package_name, "urdf"), glob("urdf/*.urdf")),
        (os.path.join("share", package_name, "urdf"), glob('urdf/REV_URDF_FULL.xacro')),
        (os.path.join("share", package_name, "urdf"), glob( 'urdf/REV_URDF_V2.xacro')),
        (os.path.join("share", package_name, "meshes"), glob('meshes/*')),
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
            'my_node = rover_description.my_node:main'
        ],
    },
)

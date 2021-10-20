# Wishlist Microservice

[![Build Status](https://app.travis-ci.com/Wishlist-Squad/wishlists.svg?branch=main)](https://app.travis-ci.com/Wishlist-Squad/wishlists)
[![codecov](https://codecov.io/gh/Wishlist-Squad/wishlists/branch/main/graph/badge.svg?token=WSM2E1CI2D)](https://codecov.io/gh/Wishlist-Squad/wishlists)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## What's featured in the project?

    * app/routes.py -- the main Service routes using Python Flask
    * app/models.py -- the data models using SQLAlchemy
    * tests/test_routes.py -- test cases against the Wishlist service
    * tests/test_models.py -- test cases against the Wishlist and Product models
    
## API Endpoints

```
Endpoint           Methods  Rule
----------------   -------  -----------------------------------------------------
index              GET      /

list_wishlists     GET      /wishlists
create_wishlists   POST     /wishlists
get_wishlists      GET      /wishlists/<wishlist_id>
update_wishlists   PUT      /wishlists/<wishlist_id>
delete_wishlists   DELETE   /wishlists/<wishlist_id>

list_products      GET      /wishlists/<int:wishlist_id>/products
create_products    POST     /wishlists/<wishlist_id>/products
get_products       GET      /wishlists/<wishlist_id>/products/<product_id>
delete_products    DELETE   /wishlists/<wishlist_id>/products/<product_id>
```

## Prerequisite Installation using Vagrant

The easiest way to use this lab is with Vagrant and VirtualBox. If you don't have this software the first step is down download and install it. If you have an 2020 Apple Mac with the M1 chip, you should download Docker Desktop instead of VirtualBox. Here is what you need:

Download: [Vagrant](https://www.vagrantup.com/)

Intel Download: [VirtualBox](https://www.virtualbox.org/)

Apple M1 Download: [Apple M1 Tech Preview](https://docs.docker.com/docker-for-mac/apple-m1/)

Install each of those. Then all you have to do is clone this repo and invoke vagrant:

### Using Vagrant and VirtualBox

```shell
git clone https://github.com/nyu-devops/lab-flask-tdd.git
cd lab-flask-tdd
vagrant up
```

### Using Vagrant and Docker Desktop

Just add `--provider docker` to the `vagrant up` command like this:

```sh
git clone https://github.com/nyu-devops/lab-flask-tdd.git
cd lab-flask-tdd
vagrant up --provider docker
```

This will use a Docker container instead of a Virtual Machine (VM). Everything else should be the same.

## Running the tests

You can now `ssh` into the virtual machine and run the service and the test suite:

```sh
vagrant ssh
cd /vagrant
```

You will now be inside the Linux virtual machine so all commands will be Linux commands.

## Running the service

The project uses *honcho* which gets it's commands from the `Procfile`. To start the service simply use:

```shell
$ honcho start
```

You should be able to reach the service at: http://localhost:5000

## Manually running the Tests

Run the tests using `nosetests`

```shell
$ nosetests
```

When you are done, you can exit and shut down the vm with:

```shell
$ exit
$ vagrant halt
```

If the VM is no longer needed you can remove it with:

```shell
$ vagrant destroy
```

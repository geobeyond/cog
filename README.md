## cog

RESTful Web API for publishing Cloud Optimized GeoTIFF to [Minio](https://www.minio.io/)
bucket and serving out of the box

[![](http://www.cogeo.org/images/logo/Cog-02.png)](http://www.cogeo.org)

[![](https://img.shields.io/badge/IBM%20Cloud-powered-blue.svg)](https://bluemix.net)
![Platform](https://img.shields.io/badge/platform-DJANGO-lightgrey.svg?style=flat)

### Table of Contents
* [Summary](#summary)
* [Requirements](#requirements)
* [Configuration](#configuration)
* [Run](#run)
* [Debug](#debug)
* [License](#license)

<a name="summary"></a>
### Summary
The Web basic starter contains an opinionated set of files for web serving:

- `app/templates/index.html`
- `staticfiles/js/bundle.js`
- `staticfiles/css/default.css`



<a name="enablement"></a>
### IBM Cloud Enablement

<a name="requirements"></a>
### Requirements
#### Local Development Tools Setup (optional)

- If you don't already have it, install [Python](https://www.python.org/downloads/)

#### IBM Cloud development tools setup (optional)

1. Install [IBM Cloud Developer Tools](https://console.bluemix.net/docs/cli/idt/setting_up_idt.html#add-cli) on your machine  
2. Install the plugin with: `bx plugin install dev -r bluemix`


#### IBM Cloud DevOps setup (optional)

[![Create Toolchain](https://console.ng.bluemix.net/devops/graphics/create_toolchain_button.png)](https://console.ng.bluemix.net/devops/setup/deploy/)

[IBM Cloud DevOps](https://www.ibm.com/cloud-computing/bluemix/devops) services provides toolchains as a set of tool integrations that support development, deployment, and operations tasks inside IBM Cloud. The "Create Toolchain" button creates a DevOps toolchain and acts as a single-click deploy to IBM Cloud including provisioning all required services. 

***Note** you must publish your project to [Github](https://github.com/) for this to work.



<a name="configuration"></a>
### Configuration

The project contains IBM Cloud specific files that are used to deploy the application as part of an IBM Cloud DevOps flow. The `.bluemix` directory contains files used to define the IBM Cloud toolchain and pipeline for your application. The `manifest.yml` file specifies the name of your application in IBM Cloud, the timeout value during deployment, and which services to bind to.

Credentials are either taken from the VCAP_SERVICES environment variable if in IBM Cloud, or from a config file if running locally. 


<a name="run"></a>
### Run
#### Using IBM Cloud development CLI
The IBM Cloud development plugin makes it easy to compile and run your application if you do not have all of the tools installed on your computer yet. Your application will be compiled with Docker containers. To compile and run your app, run:

```bash
bx dev build
bx dev run
```


#### Using your local development environment



##### Endpoints

Your application is running at: `http://localhost:3000/` in your browser.

- Health endpoint: `/health`



<a name="debug"></a>
### Debug

#### Using IBM Cloud development CLI
To build and debug your app, run:
```bash
bx dev build --debug
bx dev debug
```
#### Using your local development environment
To debug a `django` project run `python manage.py runserver` with DEBUG set to True in settings.py to start a native django development server. This comes with the Django's stack-trace debugger, which will present runtime failure stack-traces. For more information, see [Django's documentation](https://docs.djangoproject.com/en/2.0/ref/settings/).

<a name="license"></a>
### License

[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg?longCache=true&style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)
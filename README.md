# s3-ttl-lambda
Time To Live (TTL) lambda function for S3. For when the built-in s3 version is not enough

## Required software

You'll need to download and install the following software:

* [Docker Desktop](https://www.docker.com/products/docker-desktop)
* [Python 3.7](https://www.python.org/downloads/)
    * or via [homebrew](https://homebrew.sh) on osx
* [Pipenv](https://pypi.org/project/pipenv/)
* [AWS CLI](https://aws.amazon.com/cli/)
* [node via nvm](https://github.com/nvm-sh/nvm/blob/master/README.md)

Make sure you have set up AWS credentials (typically placed under `~/.aws/credentials` or `~/.aws/config`). The credentials you're using should have "enough" privileges to provision all required services. You'll know the exact definition of "enough" when you get "permission denied" errors :)

Now, indicate which AWS profile should be used by the provided scripts, e.g,:

```bash
export AWS_PROFILE=[your-aws-profile]
```

## Python environment

Create the Python virtual environment and install the dependencies:

```bash
# from the project's root directory
pipenv --python 3.7 # creates Python 3.7 virtual environment
pipenv shell    # activate the virtual environment
pipenv install  # install dependencies
pipenv install --dev # install dev dependencies
```

To know where the virtual environments and the dependencies are installed type this:

```bash
pipenv --venv
```

### Deploying the Backend

This project uses [serverless.js](https://serverless.com/) for deployment.

SAM is really good, especially when starting development, however there are some limitations that serverless.js helps us overcome because of it's plugin architecture. In particular, `serverless-python-requirements` plugin

The big thing SAM is great at is local development. Implementing a good offline/local development mode for serverless with python is still under investigation. Right now you can use `sls invoke local -f S3TTL -d '{}' --docker` but it's as slow as deploying to the cloud with a custom stage.

Note: before deploying, replace values for `s3_bucket_name: BUCKET_I_WANT_TO_TTL_OBJECTS_IN` and `TTL_HOURS: 24` in `serverless.yaml`
```bash
# to deploy the entire backend
# from the project's root directory
# be sure you have run `npm install` first
# Run following command from MacOS to ensure you do not hit the open file limit.
sudo launchctl limit maxfiles 65536 200000
# Run following command to deploy solution in dev stage
sls deploy --stage dev --enable_docker true --aws-profile customprofile
```

```bash
# to deploy a single function
sls deploy function --function S3TTL3 --stage dev --enable_docker true --aws-profile customprofile
```

- note that we are declaring the stage name to be something unrelated to `dev`, `test`, `stg`, or `prod`
- we are also making sure to use docker for packaging the python lambdas and their requirements
- we are specifying a named profile in our `~/.aws/credentials`

```bash
# to delete the stack
sls remove --stage dev --aws-profile customprofile
```

#### Adding python packages ####

- ensure you are using the virtual environment created by `pipenv` earlier
- install packages needed by the lambda
    - `pipenv install <PACKAGE>`
- install packages needed to develop
    - `pipenv install --dev <PACKAGE>`
- example Pipenv upgrade workflow
    - Find out whatâ€™s changed upstream, two options:
        - `pipenv update --outdated`
        - `pipenv run pip list --outdated`
            - this will show everything, including dependencies. be cautious of this one
    - Upgrade packages, two options:
        - Want to upgrade everything? Just do `pipenv update`
        - Want to upgrade packages one-at-a-time? `pipenv update <pkg>` for each outdated package.

#PCF Persistence Tile

This Repository is intended to allow PCF Users to deploy a Persistent Service broker in a few simple steps.

##What does it do?

[PCF Tiles](https://docs.pivotal.io/partners/deploying-with-ops-man-tile.html) are packages that provide users ease of installation by installing a tarball into their Operations Manager. This Tile will install all necessary dependencies and automatically register a service to the CF Marketplace.

The service will provide volume mounts into an Isilon cluster for [persistent storage in PCF](https://github.com/EMC-Dojo/cf-persist-service-broker).


##How can I install it?

The installation from the source is available from our [releases folder](/releases). After downloading this release, Use the OpsManager UI to Import the product, then stage it by using the `+` button on the left pane.

####Azs and networks

Ensure that the Tile is on the same Network as PCF and Isilon. Assign it's AZ accordingly.

####Isilon Configuration

There's a lot of options here that require knowledge of the Isilon cluster and a bit on the service broker, so let's take it step by step.

`Skip certificate checking` is available for users that may be using a PCF installation that doesn't have certificates signed by a CA. If you're unsure that SSL connections will properly verify, it's safe to click this just in case.

`Dell Persistent Broker Port` will provide a port for the service broker to run on. This requires some value either `80` or above `1024`. The installation will automatically set up a service broker pointing to this port, so it is not critical that this be anything specific.

`Isilon Service Name` will become the name of the plan in CF Marketplace. Be sure this doesn't use any special characters like `?!@#$*(%)&'`.

`Isilon Endpoint` is the endpoint for Isilon OneFS. This will be used by the broker to interact with the available API as of 8.0.1.

`Isilon Username` should be an Isilon user that has read and write permissions onto the Isilon cluster.

`Isilon Password` should be the password for the username above.

`Isilon Volume Path` is the path that all app data will be mounted into the Isilon volume. It is recommended to start with a slash like `/mydir`.

`Isilon NFS Host` Should be the HOST of the OneFS Isilon cluster available to the service broker. This may be different than the endpoint.

`Isilon Data Subnet` Will be the same data subnet as available to the Isilon Cluster.

`Quotas` will allow the service broker to comply with quota regulation __if it is also enabled in OneFS__.

######Errands

Both errands are recommended to be turned on. If they are not, the CC will not register the broker on install, or deregister on uninstall. You could manually install later, but using these errands is a more streamlined solution.

######Resource Config

These values should be fine. Perhaps more instances will be useful, but for most users one broker should be enough.

######Stemcell

Be sure to upload the [stemcell](http://bosh.cloudfoundry.org/stemcells) appropriate for your PCF Deployment.

After following these steps, going back to the home page and pressing 'Apply Changes' should install our broker and allow for [rexray](https://github.com/EMC-Dojo/rexray-boshrelease) to mount volumes into containers. Check out our documentation for more on that!

#PCF Isilon Tile

This Pivotal Tile enables Isilon Storage within Pivotal Cloud Foundry in a few simple steps.

##What does it do?

The Isilon Tile enables Cloud Foundry applications to read and write into Isilon Storage as if it's a local filesystem. For more information, please reference this quick [demo](http://dojoblog.emc.com/cloud-foundry/persistence-5-minutes-cloudfoundry-wahooo/).

[PCF Tiles](https://docs.pivotal.io/partners/deploying-with-ops-man-tile.html) are packages that provide users ease of installation by using Operations Manager. The Isilon Tile will install all necessary dependencies and automatically register a service to the PCF Marketplace. PCF Users can then create Isilon service instances from PCF Marketplace and access storage from Isilon in their PCF applications.

The service will provide volume mounts into an Isilon cluster for [persistent storage in PCF](https://github.com/EMC-Dojo/cf-persist-service-broker).


##How can I install it?
A complete instruction guide to install the Isilon Tile on Pivotal Cloud Foundry is published [here](http://cf-persist-service-broker.readthedocs.io/en/latest/Configuring%20PCF%20for%20Isilon/).

##Resources

- Documentation: <http://cf-persist-service-broker.readthedocs.io/>
- Slack Channel:
  - Organization: <http://cloudfoundry.slack.com>
  - Channel: `#persi`
- Email: [emcdojo@emc.com](mailto:emcdojo@emc.com)
- Twitter: [@EMCDojo](https://twitter.com/hashtag/emcdojo)
- Blog: <http://dojoblog.emc.com>

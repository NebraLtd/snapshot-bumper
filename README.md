# snapshot-bumper

**This repo has been archived and replaced by [hm-block-tracker](https://github.com/NebraLtd/hm-block-tracker)**

To try and speed up the onboarding process for customers, Nebra Helium Hotspots will download a more up to date version of the blockchain each time they are powered up.

This tool will keep a cache of blocks in a flatfile database or such to use for the blessed block, and on a cron generate a new static file which is downloaded by the hotspots on boot.

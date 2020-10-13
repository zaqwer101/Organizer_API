#!/bin/bash
docker kill organizer_api_mongo_1
rm /usr/src/Organizer_API/data/* -rf
docker start organizer_api_mongo_1
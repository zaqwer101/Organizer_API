#!/bin/bash
docker kill organizer_api_mongo_1
rm services/data/* -rf
docker start organizer_api_mongo_1

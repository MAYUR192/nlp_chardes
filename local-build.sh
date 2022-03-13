#!/bin/bash
port = 5000
docker build   --build-arg PORT=${port} -t  word_image .
docker tag word_image word_image:latest

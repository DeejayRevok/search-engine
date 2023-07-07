build_chart:
	cat VERSION | xargs -I {} helm package -u --version {} --app-version {} helm/search-engine

run_web_server:
	nohup metricbeat -e -c /etc/metricbeat/metricbeat.yml &
	nohup filebeat -e -c /etc/filebeat/filebeat.yml &
	python -m aiohttp.web -H 0.0.0.0 -P 8081 app.loaders.web_app_loader:load

run_kombu_event_consumer:
	nohup metricbeat -e -c /etc/metricbeat/metricbeat.yml &
	nohup filebeat -e -c /etc/filebeat/filebeat.yml &
	python app/kombu_event_consumer_runner.py -c $(CONSUMER_NAME)

run_kombu_iam_event_consumer:
	nohup metricbeat -e -c /etc/metricbeat/metricbeat.yml &
	nohup filebeat -e -c /etc/filebeat/filebeat.yml &
	python app/kombu_event_consumer_runner.py -c $(CONSUMER_NAME) -d infrastructure.iam.iam_passenger_json_deserializer.IAMPassengerJSONDeserializer

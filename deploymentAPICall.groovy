@Grapes([
	@Grab(group='org.codehaus.groovy.modules.http-builder', module='http-builder', version='0.7')
])

import groovyx.net.http.*

def API_KEY = "b39218cf528c8373eb7a557322149540"
def APP_ID = "1862573"
def URL = "https://api.newrelic.com/v2/applications/1862573/deployments.json"

def http = new HTTPBuilder(URL)
http.setHeaders(["X-Api-Key":"${API_KEY}", "Content-Type":"application/json"])
def json = '{"deployment": {"revision": "rev", "changelog": "Added", "description": "Added a deployments resource", "user": "me@example.com" }}' 
	
http.request(Method.POST) {
	requestContentType = ContentType.JSON
	body = json
	
	response.success = { resp, reader ->
		println "${resp.statusLine}"
		
		resp.headers.each { h ->
			println " ${h.name} : ${h.value}"
		}
	
		// ret = reader.getText() ----- this needs to be parsed as JSON
		// println ret
	}
	
	response.failure = { resp ->
		println "${resp.statusLine}"
		resp.headers.each { h ->
			println " ${h.name} : ${h.value}"
		}
		
	}
		
}

		

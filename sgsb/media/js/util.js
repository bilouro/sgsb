function getIdChamado() {
	fullDomain = window.location.href;
	dados = fullDomain.split('/');
	
	return dados[5];
}

function createHttpRequest() {
	var http_request = false;
	
	if (window.XMLHttpRequest) { // Mozilla, Safari,...
	   http_request = new XMLHttpRequest();
	   if (http_request.overrideMimeType) {
	      http_request.overrideMimeType('text/html');
	   }
	} else if (window.ActiveXObject) { // IE
	   try {
	      http_request = new ActiveXObject("Msxml2.XMLHTTP");
	   } catch (e) {
	      try {
	         http_request = new ActiveXObject("Microsoft.XMLHTTP");
	      } catch (e) {}
	   }
	}
	if (!http_request) {
	   //alert('Cannot create XMLHTTP instance');
	   return false;
	}
	return http_request;
}


function createMarker(lat, lng, imagem, titulo) {
	var point = new google.maps.LatLng(lat,lng);
	
	var marker = new google.maps.Marker({
    	position: point, 
    	map: map, 
		icon: imagem,
		title: titulo,
		draggable: true
  	});   

  	google.maps.event.addListener(marker, 'click', function() {
  		map.panTo(marker.getPosition());
  		displayDados(titulo, marker);
		infoWindow.open(map,marker);
	});
  	
	return marker;
}  	

function displayDados(titulo, marker) { 
	http_request = createHttpRequest();
	getListUrl = false;
	
	infoWindow.setContent('<div id="box" class="ui-widget-content ui-corner-all"><img src="http://www.bilouro.com/images/loading.gif" border="0" width="300" height="300"></div>');
	
	if (titulo == "Oficina") {
		item_id = oficinaMarkerManager.getId(marker);
		getListUrl = "/gpstaxi/getValorListOficina/?item="+ item_id;

		http_request.onreadystatechange = function() { processaRetornoDadosOficina(marker); }
	} else if (titulo == "Prestador") {
		posicao_id = posicaoPrestadorMarkerManager.getId(marker);
		getListUrl = "/gpstaxi/getPosicaoPrestador/"+ posicao_id + "/";

		http_request.onreadystatechange = function() { processaRetornoDadosPrestador(marker); }
	}
	

	if (getListUrl) {
		http_request.open('GET', this.getListUrl , true);
		http_request.send(null);
	} 
}

rad = function(x) {return x*Math.PI/180;}

distHaversine = function(p1, p2) {
  var R = 6371; // earth's mean radius in km
  var dLat  = rad(p2.position.lat() - p1.position.lat());
  var dLong = rad(p2.position.lng() - p1.position.lng());

  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
          Math.cos(rad(p1.position.lat())) * Math.cos(rad(p2.position.lat())) * Math.sin(dLong/2) * Math.sin(dLong/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  var d = R * c;

  return d.toFixed(3);
}
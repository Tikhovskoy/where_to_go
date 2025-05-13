// Инициализация карты
var map = L.map('map');
map.setView([55.753989, 37.623191], 11);

L.tileLayer.provider('OpenStreetMap.Mapnik').addTo(map);

// Sidebar
var sidebar = L.control.sidebar('sidebar', {
  closeButton: true,
  position: 'right'
});
map.addControl(sidebar);

// Отладочный чекбокс
L.control.custom({
  position: 'bottomleft',
  content: `
    <label>
      <input name="debug" type="checkbox" ${log.getLevel()<=1 ? 'checked' : ''}/>
      Отладка
    </label>`,
  style: {
    padding: '10px',
    background: 'rgba(255, 255, 255, 0.7)',
  },
  events: {
    click: event => {
      if (event.target.name === 'debug') {
        let level = event.target.checked ? 'debug' : 'warn';
        log.setLevel(level);
        console.log(`Set log level: ${level}`);
      }
    },
  }
}).addTo(map);

// Вспомогательная функция для чтения inline JSON
function loadJSON(elementId) {
  let el = document.getElementById(elementId);
  if (!el) {
    log.error(`Not found element with id '${elementId}'.`);
    return null;
  }
  return JSON.parse(el.textContent);
}

let places = loadJSON('places-geojson');
log.debug('Load GeoJSON for places', places);

// Добавляем маркеры
L.geoJSON(places, {
  pointToLayer: function(feature, latlng) {
    let color = feature.properties.color || 'red';
    let pulsingIcon = L.icon.pulse({
      iconSize: [12, 12],
      color: color,
      fillColor: color,
      heartbeat: 2.5,
    });
    let marker = L.marker(latlng, {
      icon: pulsingIcon,
      riseOnHover: true,
    });
    marker.bindTooltip(feature.properties.title);
    marker.bindPopup(feature.properties.title);
    marker.on('click', function() {
      log.debug('Feature selected', feature);
      sidebar.show();
      loadPlaceInfo(feature.properties.placeId, feature.properties.detailsUrl);
    });
    return marker;
  }
}).addTo(map);

// Vue.js приложение в сайдбаре
var sidebarApp = new Vue({
  el: '#sidebar-app',
  template: document.getElementById('app-template').innerHTML,
  data: {
    loadingPlaceId: null,
    selectedPlace: null,
  },
  computed: {
    promptVisible() {
      return !this.loading && !this.selectedPlace;
    },
    loading() {
      return this.loadingPlaceId !== null;
    },
    mainPhotoSrc() {
      return this.selectedPlace && this.selectedPlace.imgs.length
        ? this.selectedPlace.imgs[0]
        : null;
    },
    carouselImgs() {
      return this.selectedPlace && this.selectedPlace.imgs.length
        ? this.selectedPlace.imgs.slice(1)
        : [];
    },
  },
  updated() {
    this.$nextTick(() => {
      $('#place-photos').carousel();
    });
  },
  methods: {
    handlePhotosClick(slideId = 'next') {
      $('#place-photos').carousel(slideId);
    },
  },
});

// Сброс при клике вне маркера
map.on('click', () => {
  sidebarApp.selectedPlace = null;
  sidebarApp.loadingPlaceId = null;
});

// Загрузка детальной информации
async function loadPlaceInfo(placeId, detailsUrl) {
  sidebarApp.selectedPlace = null;
  sidebarApp.loadingPlaceId = placeId;

  try {
    let response = await fetch(detailsUrl);
    if (!response.ok) return;
    let data = await response.json();
    if (sidebarApp.loadingPlaceId !== placeId) return;

    sidebarApp.selectedPlace = {
      title: data.title,
      placeId: placeId,
      imgs: data.imgs || [],
      short_description: data.description_short,
      long_description: data.description_long,
    };
  } finally {
    if (sidebarApp.loadingPlaceId === placeId) {
      sidebarApp.loadingPlaceId = null;
    }
  }
}
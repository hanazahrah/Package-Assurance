//node js to influxdb
const {InfluxDB} = require('@influxdata/influxdb-client')

// You can generate a Token from the "Tokens Tab" in the UI
const token = ''
const org = ''
const bucket = ''

//ganti url influxdb dengan wifi sendiri
const client = new InfluxDB({url: '', token: token})

const {Point} = require('@influxdata/influxdb-client')
const writeApi = client.getWriteApi(org, bucket)
writeApi.useDefaultTags({host: 'host1'})



// controller.js
const mqtt = require('mqtt')
//const client = mqtt.connect('mqtt://36.92.136.155:31883') //1883
//options={
//  clientId:"local",
//  username:"mqtt",
//  password:"coba",
//  clean:true};
  
const client2 = mqtt.connect('mqtt://test.mosquitto.org:1883')
 
//const client = mqtt.connect('mqtt://broker.emqx.io:1883')
const fs = require('fs');

var garageState = ''
var connected = false

client2.on('connect', () => {
  client2.subscribe('/DataTest')
})

client2.on('message', (topic, message) => {
  //if(topic === 'ANTARES/DataTest') {
//    connected = (message.toString() === 'true');
    let txt = message.toString()
    let arr = txt.split(",")
    console.log(txt)
    const point = new Point('fall')
  .tag('id', arr[0])
  .floatField('accelX', arr[1])
  .floatField('accelY', arr[2])
  .floatField('accelZ', arr[3])
  .floatField('accelSqrt', arr[4])
  .floatField('gyroX', arr[5])
  .floatField('gyroY', arr[6])
  .floatField('gyroZ', arr[7])
  .floatField('magX', arr[8])
  .floatField('magY', arr[9])
  .floatField('magZ', arr[10])
  .floatField('hDir', arr[11])
  .floatField('label', arr[12])
writeApi.writePoint(point)
//writeApi
//    .close()
//    .then(() => {
//        console.log('FINISHED')
//    })
//    .catch(e => {
//        console.error(e)
//        console.log('\\nFinished ERROR')
//    })
    //fs.appendFile('message.txt', message.toString(), function (err) {
    //  if (err) throw err;
    //  console.log('Saved!');
    //});
  //}
})
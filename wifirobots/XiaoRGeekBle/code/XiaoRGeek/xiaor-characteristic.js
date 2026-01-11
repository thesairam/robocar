var util = require('util');
var os = require('os');
var exec = require('child_process').exec;

var bleno = require('../..');

var Descriptor = bleno.Descriptor;
var Characteristic = bleno.Characteristic;

var net = require('net');
//创建TCP客户端
var client = new net.Socket();
client.setEncoding('utf8');
client.connect(2002,'localhost',function () {
    console.log('已连接到服务器');
});


var XiaoRCharacteristic = function() {
  XiaoRCharacteristic.super_.call(this, {
     uuid: '0000ffe1-0000-1000-8000-00805f9b34fb',
    properties: ['write', 'writeWithoutResponse']
  });
};

util.inherits(XiaoRCharacteristic, Characteristic);

XiaoRCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
  console.log('WriteOnlyCharacteristic write request: ' + data.toString('hex') + ' ' + offset + ' ' + withoutResponse);
  client.write(data);
  callback(this.RESULT_SUCCESS);
};

module.exports = XiaoRCharacteristic;

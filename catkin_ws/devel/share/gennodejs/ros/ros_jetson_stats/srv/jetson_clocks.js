// Auto-generated. Do not edit!

// (in-package ros_jetson_stats.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class jetson_clocksRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.status = null;
    }
    else {
      if (initObj.hasOwnProperty('status')) {
        this.status = initObj.status
      }
      else {
        this.status = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type jetson_clocksRequest
    // Serialize message field [status]
    bufferOffset = _serializer.bool(obj.status, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type jetson_clocksRequest
    let len;
    let data = new jetson_clocksRequest(null);
    // Deserialize message field [status]
    data.status = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_jetson_stats/jetson_clocksRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '3a1255d4d998bd4d6585c64639b5ee9a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # jetson_clocks selection
    
    bool status
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new jetson_clocksRequest(null);
    if (msg.status !== undefined) {
      resolved.status = msg.status;
    }
    else {
      resolved.status = false
    }

    return resolved;
    }
};

class jetson_clocksResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.return = null;
    }
    else {
      if (initObj.hasOwnProperty('return')) {
        this.return = initObj.return
      }
      else {
        this.return = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type jetson_clocksResponse
    // Serialize message field [return]
    bufferOffset = _serializer.bool(obj.return, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type jetson_clocksResponse
    let len;
    let data = new jetson_clocksResponse(null);
    // Deserialize message field [return]
    data.return = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_jetson_stats/jetson_clocksResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '88eeb9c2a71b8e1ccaf759811ce45dd0';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool return
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new jetson_clocksResponse(null);
    if (msg.return !== undefined) {
      resolved.return = msg.return;
    }
    else {
      resolved.return = false
    }

    return resolved;
    }
};

module.exports = {
  Request: jetson_clocksRequest,
  Response: jetson_clocksResponse,
  md5sum() { return '8c3d867c150b13d0a3fcbf4f14955089'; },
  datatype() { return 'ros_jetson_stats/jetson_clocks'; }
};

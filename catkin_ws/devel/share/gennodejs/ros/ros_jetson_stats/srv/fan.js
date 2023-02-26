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

class fanRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.mode = null;
      this.fanSpeed = null;
    }
    else {
      if (initObj.hasOwnProperty('mode')) {
        this.mode = initObj.mode
      }
      else {
        this.mode = '';
      }
      if (initObj.hasOwnProperty('fanSpeed')) {
        this.fanSpeed = initObj.fanSpeed
      }
      else {
        this.fanSpeed = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type fanRequest
    // Serialize message field [mode]
    bufferOffset = _serializer.string(obj.mode, buffer, bufferOffset);
    // Serialize message field [fanSpeed]
    bufferOffset = _serializer.int8(obj.fanSpeed, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type fanRequest
    let len;
    let data = new fanRequest(null);
    // Deserialize message field [mode]
    data.mode = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [fanSpeed]
    data.fanSpeed = _deserializer.int8(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.mode.length;
    return length + 5;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_jetson_stats/fanRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'a40184a9984237fb3cdc8207761a7cfe';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # fan selection
    
    string mode
    int8 fanSpeed
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new fanRequest(null);
    if (msg.mode !== undefined) {
      resolved.mode = msg.mode;
    }
    else {
      resolved.mode = ''
    }

    if (msg.fanSpeed !== undefined) {
      resolved.fanSpeed = msg.fanSpeed;
    }
    else {
      resolved.fanSpeed = 0
    }

    return resolved;
    }
};

class fanResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.done = null;
    }
    else {
      if (initObj.hasOwnProperty('done')) {
        this.done = initObj.done
      }
      else {
        this.done = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type fanResponse
    // Serialize message field [done]
    bufferOffset = _serializer.string(obj.done, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type fanResponse
    let len;
    let data = new fanResponse(null);
    // Deserialize message field [done]
    data.done = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.done.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_jetson_stats/fanResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '6f6f8833c91017f802acaa131839007d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string done
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new fanResponse(null);
    if (msg.done !== undefined) {
      resolved.done = msg.done;
    }
    else {
      resolved.done = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: fanRequest,
  Response: fanResponse,
  md5sum() { return 'f745cc3cd10b95c8e8f7fabace50fbb1'; },
  datatype() { return 'ros_jetson_stats/fan'; }
};

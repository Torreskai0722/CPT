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

class nvpmodelRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.nvpmodel = null;
    }
    else {
      if (initObj.hasOwnProperty('nvpmodel')) {
        this.nvpmodel = initObj.nvpmodel
      }
      else {
        this.nvpmodel = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type nvpmodelRequest
    // Serialize message field [nvpmodel]
    bufferOffset = _serializer.string(obj.nvpmodel, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type nvpmodelRequest
    let len;
    let data = new nvpmodelRequest(null);
    // Deserialize message field [nvpmodel]
    data.nvpmodel = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.nvpmodel.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_jetson_stats/nvpmodelRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '0fac0d4a363e336a74a2265c4c0f32e9';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # NV Power Model selection
    
    string nvpmodel
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new nvpmodelRequest(null);
    if (msg.nvpmodel !== undefined) {
      resolved.nvpmodel = msg.nvpmodel;
    }
    else {
      resolved.nvpmodel = ''
    }

    return resolved;
    }
};

class nvpmodelResponse {
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
        this.return = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type nvpmodelResponse
    // Serialize message field [return]
    bufferOffset = _serializer.string(obj.return, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type nvpmodelResponse
    let len;
    let data = new nvpmodelResponse(null);
    // Deserialize message field [return]
    data.return = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.return.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'ros_jetson_stats/nvpmodelResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '8d02df2c0dff1a16a80230979e550820';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string return
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new nvpmodelResponse(null);
    if (msg.return !== undefined) {
      resolved.return = msg.return;
    }
    else {
      resolved.return = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: nvpmodelRequest,
  Response: nvpmodelResponse,
  md5sum() { return '7942b12339fc624078e7a634375396ac'; },
  datatype() { return 'ros_jetson_stats/nvpmodel'; }
};

// Auto-generated. Do not edit!

// (in-package ros_referee.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class ProcessStatus {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.pid = null;
      this.ppid = null;
      this.cpids = null;
      this.scheduling_policy = null;
      this.priority = null;
      this.imgseq = null;
      this.app = null;
      this.runtime = null;
      this.proposals = null;
      this.objects = null;
      this.probability = null;
      this.data = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('pid')) {
        this.pid = initObj.pid
      }
      else {
        this.pid = 0;
      }
      if (initObj.hasOwnProperty('ppid')) {
        this.ppid = initObj.ppid
      }
      else {
        this.ppid = 0;
      }
      if (initObj.hasOwnProperty('cpids')) {
        this.cpids = initObj.cpids
      }
      else {
        this.cpids = [];
      }
      if (initObj.hasOwnProperty('scheduling_policy')) {
        this.scheduling_policy = initObj.scheduling_policy
      }
      else {
        this.scheduling_policy = '';
      }
      if (initObj.hasOwnProperty('priority')) {
        this.priority = initObj.priority
      }
      else {
        this.priority = 0;
      }
      if (initObj.hasOwnProperty('imgseq')) {
        this.imgseq = initObj.imgseq
      }
      else {
        this.imgseq = 0;
      }
      if (initObj.hasOwnProperty('app')) {
        this.app = initObj.app
      }
      else {
        this.app = '';
      }
      if (initObj.hasOwnProperty('runtime')) {
        this.runtime = initObj.runtime
      }
      else {
        this.runtime = 0.0;
      }
      if (initObj.hasOwnProperty('proposals')) {
        this.proposals = initObj.proposals
      }
      else {
        this.proposals = 0;
      }
      if (initObj.hasOwnProperty('objects')) {
        this.objects = initObj.objects
      }
      else {
        this.objects = 0;
      }
      if (initObj.hasOwnProperty('probability')) {
        this.probability = initObj.probability
      }
      else {
        this.probability = [];
      }
      if (initObj.hasOwnProperty('data')) {
        this.data = initObj.data
      }
      else {
        this.data = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ProcessStatus
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [pid]
    bufferOffset = _serializer.int64(obj.pid, buffer, bufferOffset);
    // Serialize message field [ppid]
    bufferOffset = _serializer.int64(obj.ppid, buffer, bufferOffset);
    // Serialize message field [cpids]
    bufferOffset = _arraySerializer.int64(obj.cpids, buffer, bufferOffset, null);
    // Serialize message field [scheduling_policy]
    bufferOffset = _serializer.string(obj.scheduling_policy, buffer, bufferOffset);
    // Serialize message field [priority]
    bufferOffset = _serializer.uint8(obj.priority, buffer, bufferOffset);
    // Serialize message field [imgseq]
    bufferOffset = _serializer.int64(obj.imgseq, buffer, bufferOffset);
    // Serialize message field [app]
    bufferOffset = _serializer.string(obj.app, buffer, bufferOffset);
    // Serialize message field [runtime]
    bufferOffset = _serializer.float64(obj.runtime, buffer, bufferOffset);
    // Serialize message field [proposals]
    bufferOffset = _serializer.int64(obj.proposals, buffer, bufferOffset);
    // Serialize message field [objects]
    bufferOffset = _serializer.int64(obj.objects, buffer, bufferOffset);
    // Serialize message field [probability]
    bufferOffset = _arraySerializer.float64(obj.probability, buffer, bufferOffset, null);
    // Serialize message field [data]
    bufferOffset = _arraySerializer.int64(obj.data, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ProcessStatus
    let len;
    let data = new ProcessStatus(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [pid]
    data.pid = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [ppid]
    data.ppid = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [cpids]
    data.cpids = _arrayDeserializer.int64(buffer, bufferOffset, null)
    // Deserialize message field [scheduling_policy]
    data.scheduling_policy = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [priority]
    data.priority = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [imgseq]
    data.imgseq = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [app]
    data.app = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [runtime]
    data.runtime = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [proposals]
    data.proposals = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [objects]
    data.objects = _deserializer.int64(buffer, bufferOffset);
    // Deserialize message field [probability]
    data.probability = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [data]
    data.data = _arrayDeserializer.int64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += 8 * object.cpids.length;
    length += object.scheduling_policy.length;
    length += object.app.length;
    length += 8 * object.probability.length;
    length += 8 * object.data.length;
    return length + 69;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ros_referee/ProcessStatus';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '60f0fccd1643b5091802875556e45e83';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    
    int64 pid
    int64 ppid
    int64[] cpids
    string scheduling_policy
    uint8 priority
    int64 imgseq
    string app
    float64 runtime
    int64 proposals
    int64 objects
    float64[] probability
    int64[] data
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    string frame_id
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ProcessStatus(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.pid !== undefined) {
      resolved.pid = msg.pid;
    }
    else {
      resolved.pid = 0
    }

    if (msg.ppid !== undefined) {
      resolved.ppid = msg.ppid;
    }
    else {
      resolved.ppid = 0
    }

    if (msg.cpids !== undefined) {
      resolved.cpids = msg.cpids;
    }
    else {
      resolved.cpids = []
    }

    if (msg.scheduling_policy !== undefined) {
      resolved.scheduling_policy = msg.scheduling_policy;
    }
    else {
      resolved.scheduling_policy = ''
    }

    if (msg.priority !== undefined) {
      resolved.priority = msg.priority;
    }
    else {
      resolved.priority = 0
    }

    if (msg.imgseq !== undefined) {
      resolved.imgseq = msg.imgseq;
    }
    else {
      resolved.imgseq = 0
    }

    if (msg.app !== undefined) {
      resolved.app = msg.app;
    }
    else {
      resolved.app = ''
    }

    if (msg.runtime !== undefined) {
      resolved.runtime = msg.runtime;
    }
    else {
      resolved.runtime = 0.0
    }

    if (msg.proposals !== undefined) {
      resolved.proposals = msg.proposals;
    }
    else {
      resolved.proposals = 0
    }

    if (msg.objects !== undefined) {
      resolved.objects = msg.objects;
    }
    else {
      resolved.objects = 0
    }

    if (msg.probability !== undefined) {
      resolved.probability = msg.probability;
    }
    else {
      resolved.probability = []
    }

    if (msg.data !== undefined) {
      resolved.data = msg.data;
    }
    else {
      resolved.data = []
    }

    return resolved;
    }
};

module.exports = ProcessStatus;

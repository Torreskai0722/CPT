; Auto-generated. Do not edit!


(cl:in-package ros_jetson_stats-srv)


;//! \htmlinclude jetson_clocks-request.msg.html

(cl:defclass <jetson_clocks-request> (roslisp-msg-protocol:ros-message)
  ((status
    :reader status
    :initarg :status
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass jetson_clocks-request (<jetson_clocks-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <jetson_clocks-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'jetson_clocks-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_jetson_stats-srv:<jetson_clocks-request> is deprecated: use ros_jetson_stats-srv:jetson_clocks-request instead.")))

(cl:ensure-generic-function 'status-val :lambda-list '(m))
(cl:defmethod status-val ((m <jetson_clocks-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_jetson_stats-srv:status-val is deprecated.  Use ros_jetson_stats-srv:status instead.")
  (status m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <jetson_clocks-request>) ostream)
  "Serializes a message object of type '<jetson_clocks-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'status) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <jetson_clocks-request>) istream)
  "Deserializes a message object of type '<jetson_clocks-request>"
    (cl:setf (cl:slot-value msg 'status) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<jetson_clocks-request>)))
  "Returns string type for a service object of type '<jetson_clocks-request>"
  "ros_jetson_stats/jetson_clocksRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'jetson_clocks-request)))
  "Returns string type for a service object of type 'jetson_clocks-request"
  "ros_jetson_stats/jetson_clocksRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<jetson_clocks-request>)))
  "Returns md5sum for a message object of type '<jetson_clocks-request>"
  "8c3d867c150b13d0a3fcbf4f14955089")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'jetson_clocks-request)))
  "Returns md5sum for a message object of type 'jetson_clocks-request"
  "8c3d867c150b13d0a3fcbf4f14955089")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<jetson_clocks-request>)))
  "Returns full string definition for message of type '<jetson_clocks-request>"
  (cl:format cl:nil "# jetson_clocks selection~%~%bool status~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'jetson_clocks-request)))
  "Returns full string definition for message of type 'jetson_clocks-request"
  (cl:format cl:nil "# jetson_clocks selection~%~%bool status~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <jetson_clocks-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <jetson_clocks-request>))
  "Converts a ROS message object to a list"
  (cl:list 'jetson_clocks-request
    (cl:cons ':status (status msg))
))
;//! \htmlinclude jetson_clocks-response.msg.html

(cl:defclass <jetson_clocks-response> (roslisp-msg-protocol:ros-message)
  ((return
    :reader return
    :initarg :return
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass jetson_clocks-response (<jetson_clocks-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <jetson_clocks-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'jetson_clocks-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_jetson_stats-srv:<jetson_clocks-response> is deprecated: use ros_jetson_stats-srv:jetson_clocks-response instead.")))

(cl:ensure-generic-function 'return-val :lambda-list '(m))
(cl:defmethod return-val ((m <jetson_clocks-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_jetson_stats-srv:return-val is deprecated.  Use ros_jetson_stats-srv:return instead.")
  (return m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <jetson_clocks-response>) ostream)
  "Serializes a message object of type '<jetson_clocks-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'return) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <jetson_clocks-response>) istream)
  "Deserializes a message object of type '<jetson_clocks-response>"
    (cl:setf (cl:slot-value msg 'return) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<jetson_clocks-response>)))
  "Returns string type for a service object of type '<jetson_clocks-response>"
  "ros_jetson_stats/jetson_clocksResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'jetson_clocks-response)))
  "Returns string type for a service object of type 'jetson_clocks-response"
  "ros_jetson_stats/jetson_clocksResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<jetson_clocks-response>)))
  "Returns md5sum for a message object of type '<jetson_clocks-response>"
  "8c3d867c150b13d0a3fcbf4f14955089")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'jetson_clocks-response)))
  "Returns md5sum for a message object of type 'jetson_clocks-response"
  "8c3d867c150b13d0a3fcbf4f14955089")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<jetson_clocks-response>)))
  "Returns full string definition for message of type '<jetson_clocks-response>"
  (cl:format cl:nil "bool return~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'jetson_clocks-response)))
  "Returns full string definition for message of type 'jetson_clocks-response"
  (cl:format cl:nil "bool return~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <jetson_clocks-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <jetson_clocks-response>))
  "Converts a ROS message object to a list"
  (cl:list 'jetson_clocks-response
    (cl:cons ':return (return msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'jetson_clocks)))
  'jetson_clocks-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'jetson_clocks)))
  'jetson_clocks-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'jetson_clocks)))
  "Returns string type for a service object of type '<jetson_clocks>"
  "ros_jetson_stats/jetson_clocks")
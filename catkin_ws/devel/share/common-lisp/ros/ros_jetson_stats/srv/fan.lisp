; Auto-generated. Do not edit!


(cl:in-package ros_jetson_stats-srv)


;//! \htmlinclude fan-request.msg.html

(cl:defclass <fan-request> (roslisp-msg-protocol:ros-message)
  ((mode
    :reader mode
    :initarg :mode
    :type cl:string
    :initform "")
   (fanSpeed
    :reader fanSpeed
    :initarg :fanSpeed
    :type cl:fixnum
    :initform 0))
)

(cl:defclass fan-request (<fan-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <fan-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'fan-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_jetson_stats-srv:<fan-request> is deprecated: use ros_jetson_stats-srv:fan-request instead.")))

(cl:ensure-generic-function 'mode-val :lambda-list '(m))
(cl:defmethod mode-val ((m <fan-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_jetson_stats-srv:mode-val is deprecated.  Use ros_jetson_stats-srv:mode instead.")
  (mode m))

(cl:ensure-generic-function 'fanSpeed-val :lambda-list '(m))
(cl:defmethod fanSpeed-val ((m <fan-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_jetson_stats-srv:fanSpeed-val is deprecated.  Use ros_jetson_stats-srv:fanSpeed instead.")
  (fanSpeed m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <fan-request>) ostream)
  "Serializes a message object of type '<fan-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'mode))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'mode))
  (cl:let* ((signed (cl:slot-value msg 'fanSpeed)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <fan-request>) istream)
  "Deserializes a message object of type '<fan-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'mode) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'mode) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'fanSpeed) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<fan-request>)))
  "Returns string type for a service object of type '<fan-request>"
  "ros_jetson_stats/fanRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'fan-request)))
  "Returns string type for a service object of type 'fan-request"
  "ros_jetson_stats/fanRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<fan-request>)))
  "Returns md5sum for a message object of type '<fan-request>"
  "f745cc3cd10b95c8e8f7fabace50fbb1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'fan-request)))
  "Returns md5sum for a message object of type 'fan-request"
  "f745cc3cd10b95c8e8f7fabace50fbb1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<fan-request>)))
  "Returns full string definition for message of type '<fan-request>"
  (cl:format cl:nil "# fan selection~%~%string mode~%int8 fanSpeed~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'fan-request)))
  "Returns full string definition for message of type 'fan-request"
  (cl:format cl:nil "# fan selection~%~%string mode~%int8 fanSpeed~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <fan-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'mode))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <fan-request>))
  "Converts a ROS message object to a list"
  (cl:list 'fan-request
    (cl:cons ':mode (mode msg))
    (cl:cons ':fanSpeed (fanSpeed msg))
))
;//! \htmlinclude fan-response.msg.html

(cl:defclass <fan-response> (roslisp-msg-protocol:ros-message)
  ((done
    :reader done
    :initarg :done
    :type cl:string
    :initform ""))
)

(cl:defclass fan-response (<fan-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <fan-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'fan-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_jetson_stats-srv:<fan-response> is deprecated: use ros_jetson_stats-srv:fan-response instead.")))

(cl:ensure-generic-function 'done-val :lambda-list '(m))
(cl:defmethod done-val ((m <fan-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_jetson_stats-srv:done-val is deprecated.  Use ros_jetson_stats-srv:done instead.")
  (done m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <fan-response>) ostream)
  "Serializes a message object of type '<fan-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'done))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'done))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <fan-response>) istream)
  "Deserializes a message object of type '<fan-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'done) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'done) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<fan-response>)))
  "Returns string type for a service object of type '<fan-response>"
  "ros_jetson_stats/fanResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'fan-response)))
  "Returns string type for a service object of type 'fan-response"
  "ros_jetson_stats/fanResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<fan-response>)))
  "Returns md5sum for a message object of type '<fan-response>"
  "f745cc3cd10b95c8e8f7fabace50fbb1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'fan-response)))
  "Returns md5sum for a message object of type 'fan-response"
  "f745cc3cd10b95c8e8f7fabace50fbb1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<fan-response>)))
  "Returns full string definition for message of type '<fan-response>"
  (cl:format cl:nil "string done~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'fan-response)))
  "Returns full string definition for message of type 'fan-response"
  (cl:format cl:nil "string done~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <fan-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'done))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <fan-response>))
  "Converts a ROS message object to a list"
  (cl:list 'fan-response
    (cl:cons ':done (done msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'fan)))
  'fan-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'fan)))
  'fan-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'fan)))
  "Returns string type for a service object of type '<fan>"
  "ros_jetson_stats/fan")
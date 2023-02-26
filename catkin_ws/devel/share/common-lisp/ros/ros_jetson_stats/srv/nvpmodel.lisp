; Auto-generated. Do not edit!


(cl:in-package ros_jetson_stats-srv)


;//! \htmlinclude nvpmodel-request.msg.html

(cl:defclass <nvpmodel-request> (roslisp-msg-protocol:ros-message)
  ((nvpmodel
    :reader nvpmodel
    :initarg :nvpmodel
    :type cl:string
    :initform ""))
)

(cl:defclass nvpmodel-request (<nvpmodel-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <nvpmodel-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'nvpmodel-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_jetson_stats-srv:<nvpmodel-request> is deprecated: use ros_jetson_stats-srv:nvpmodel-request instead.")))

(cl:ensure-generic-function 'nvpmodel-val :lambda-list '(m))
(cl:defmethod nvpmodel-val ((m <nvpmodel-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_jetson_stats-srv:nvpmodel-val is deprecated.  Use ros_jetson_stats-srv:nvpmodel instead.")
  (nvpmodel m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <nvpmodel-request>) ostream)
  "Serializes a message object of type '<nvpmodel-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'nvpmodel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'nvpmodel))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <nvpmodel-request>) istream)
  "Deserializes a message object of type '<nvpmodel-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'nvpmodel) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'nvpmodel) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<nvpmodel-request>)))
  "Returns string type for a service object of type '<nvpmodel-request>"
  "ros_jetson_stats/nvpmodelRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'nvpmodel-request)))
  "Returns string type for a service object of type 'nvpmodel-request"
  "ros_jetson_stats/nvpmodelRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<nvpmodel-request>)))
  "Returns md5sum for a message object of type '<nvpmodel-request>"
  "7942b12339fc624078e7a634375396ac")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'nvpmodel-request)))
  "Returns md5sum for a message object of type 'nvpmodel-request"
  "7942b12339fc624078e7a634375396ac")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<nvpmodel-request>)))
  "Returns full string definition for message of type '<nvpmodel-request>"
  (cl:format cl:nil "# NV Power Model selection~%~%string nvpmodel~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'nvpmodel-request)))
  "Returns full string definition for message of type 'nvpmodel-request"
  (cl:format cl:nil "# NV Power Model selection~%~%string nvpmodel~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <nvpmodel-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'nvpmodel))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <nvpmodel-request>))
  "Converts a ROS message object to a list"
  (cl:list 'nvpmodel-request
    (cl:cons ':nvpmodel (nvpmodel msg))
))
;//! \htmlinclude nvpmodel-response.msg.html

(cl:defclass <nvpmodel-response> (roslisp-msg-protocol:ros-message)
  ((return
    :reader return
    :initarg :return
    :type cl:string
    :initform ""))
)

(cl:defclass nvpmodel-response (<nvpmodel-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <nvpmodel-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'nvpmodel-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ros_jetson_stats-srv:<nvpmodel-response> is deprecated: use ros_jetson_stats-srv:nvpmodel-response instead.")))

(cl:ensure-generic-function 'return-val :lambda-list '(m))
(cl:defmethod return-val ((m <nvpmodel-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ros_jetson_stats-srv:return-val is deprecated.  Use ros_jetson_stats-srv:return instead.")
  (return m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <nvpmodel-response>) ostream)
  "Serializes a message object of type '<nvpmodel-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'return))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'return))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <nvpmodel-response>) istream)
  "Deserializes a message object of type '<nvpmodel-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'return) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'return) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<nvpmodel-response>)))
  "Returns string type for a service object of type '<nvpmodel-response>"
  "ros_jetson_stats/nvpmodelResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'nvpmodel-response)))
  "Returns string type for a service object of type 'nvpmodel-response"
  "ros_jetson_stats/nvpmodelResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<nvpmodel-response>)))
  "Returns md5sum for a message object of type '<nvpmodel-response>"
  "7942b12339fc624078e7a634375396ac")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'nvpmodel-response)))
  "Returns md5sum for a message object of type 'nvpmodel-response"
  "7942b12339fc624078e7a634375396ac")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<nvpmodel-response>)))
  "Returns full string definition for message of type '<nvpmodel-response>"
  (cl:format cl:nil "string return~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'nvpmodel-response)))
  "Returns full string definition for message of type 'nvpmodel-response"
  (cl:format cl:nil "string return~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <nvpmodel-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'return))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <nvpmodel-response>))
  "Converts a ROS message object to a list"
  (cl:list 'nvpmodel-response
    (cl:cons ':return (return msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'nvpmodel)))
  'nvpmodel-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'nvpmodel)))
  'nvpmodel-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'nvpmodel)))
  "Returns string type for a service object of type '<nvpmodel>"
  "ros_jetson_stats/nvpmodel")
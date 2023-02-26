;; Auto-generated. Do not edit!


(when (boundp 'ros_jetson_stats::jetson_clocks)
  (if (not (find-package "ROS_JETSON_STATS"))
    (make-package "ROS_JETSON_STATS"))
  (shadow 'jetson_clocks (find-package "ROS_JETSON_STATS")))
(unless (find-package "ROS_JETSON_STATS::JETSON_CLOCKS")
  (make-package "ROS_JETSON_STATS::JETSON_CLOCKS"))
(unless (find-package "ROS_JETSON_STATS::JETSON_CLOCKSREQUEST")
  (make-package "ROS_JETSON_STATS::JETSON_CLOCKSREQUEST"))
(unless (find-package "ROS_JETSON_STATS::JETSON_CLOCKSRESPONSE")
  (make-package "ROS_JETSON_STATS::JETSON_CLOCKSRESPONSE"))

(in-package "ROS")





(defclass ros_jetson_stats::jetson_clocksRequest
  :super ros::object
  :slots (_status ))

(defmethod ros_jetson_stats::jetson_clocksRequest
  (:init
   (&key
    ((:status __status) nil)
    )
   (send-super :init)
   (setq _status __status)
   self)
  (:status
   (&optional __status)
   (if __status (setq _status __status)) _status)
  (:serialization-length
   ()
   (+
    ;; bool _status
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _status
       (if _status (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _status
     (setq _status (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass ros_jetson_stats::jetson_clocksResponse
  :super ros::object
  :slots (_return ))

(defmethod ros_jetson_stats::jetson_clocksResponse
  (:init
   (&key
    ((:return __return) nil)
    )
   (send-super :init)
   (setq _return __return)
   self)
  (:return
   (&optional __return)
   (if __return (setq _return __return)) _return)
  (:serialization-length
   ()
   (+
    ;; bool _return
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _return
       (if _return (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _return
     (setq _return (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass ros_jetson_stats::jetson_clocks
  :super ros::object
  :slots ())

(setf (get ros_jetson_stats::jetson_clocks :md5sum-) "8c3d867c150b13d0a3fcbf4f14955089")
(setf (get ros_jetson_stats::jetson_clocks :datatype-) "ros_jetson_stats/jetson_clocks")
(setf (get ros_jetson_stats::jetson_clocks :request) ros_jetson_stats::jetson_clocksRequest)
(setf (get ros_jetson_stats::jetson_clocks :response) ros_jetson_stats::jetson_clocksResponse)

(defmethod ros_jetson_stats::jetson_clocksRequest
  (:response () (instance ros_jetson_stats::jetson_clocksResponse :init)))

(setf (get ros_jetson_stats::jetson_clocksRequest :md5sum-) "8c3d867c150b13d0a3fcbf4f14955089")
(setf (get ros_jetson_stats::jetson_clocksRequest :datatype-) "ros_jetson_stats/jetson_clocksRequest")
(setf (get ros_jetson_stats::jetson_clocksRequest :definition-)
      "# jetson_clocks selection

bool status
---
bool return
")

(setf (get ros_jetson_stats::jetson_clocksResponse :md5sum-) "8c3d867c150b13d0a3fcbf4f14955089")
(setf (get ros_jetson_stats::jetson_clocksResponse :datatype-) "ros_jetson_stats/jetson_clocksResponse")
(setf (get ros_jetson_stats::jetson_clocksResponse :definition-)
      "# jetson_clocks selection

bool status
---
bool return
")



(provide :ros_jetson_stats/jetson_clocks "8c3d867c150b13d0a3fcbf4f14955089")



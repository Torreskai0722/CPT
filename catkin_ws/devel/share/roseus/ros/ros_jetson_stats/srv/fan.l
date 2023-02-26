;; Auto-generated. Do not edit!


(when (boundp 'ros_jetson_stats::fan)
  (if (not (find-package "ROS_JETSON_STATS"))
    (make-package "ROS_JETSON_STATS"))
  (shadow 'fan (find-package "ROS_JETSON_STATS")))
(unless (find-package "ROS_JETSON_STATS::FAN")
  (make-package "ROS_JETSON_STATS::FAN"))
(unless (find-package "ROS_JETSON_STATS::FANREQUEST")
  (make-package "ROS_JETSON_STATS::FANREQUEST"))
(unless (find-package "ROS_JETSON_STATS::FANRESPONSE")
  (make-package "ROS_JETSON_STATS::FANRESPONSE"))

(in-package "ROS")





(defclass ros_jetson_stats::fanRequest
  :super ros::object
  :slots (_mode _fanSpeed ))

(defmethod ros_jetson_stats::fanRequest
  (:init
   (&key
    ((:mode __mode) "")
    ((:fanSpeed __fanSpeed) 0)
    )
   (send-super :init)
   (setq _mode (string __mode))
   (setq _fanSpeed (round __fanSpeed))
   self)
  (:mode
   (&optional __mode)
   (if __mode (setq _mode __mode)) _mode)
  (:fanSpeed
   (&optional __fanSpeed)
   (if __fanSpeed (setq _fanSpeed __fanSpeed)) _fanSpeed)
  (:serialization-length
   ()
   (+
    ;; string _mode
    4 (length _mode)
    ;; int8 _fanSpeed
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _mode
       (write-long (length _mode) s) (princ _mode s)
     ;; int8 _fanSpeed
       (write-byte _fanSpeed s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _mode
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _mode (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int8 _fanSpeed
     (setq _fanSpeed (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _fanSpeed 127) (setq _fanSpeed (- _fanSpeed 256)))
   ;;
   self)
  )

(defclass ros_jetson_stats::fanResponse
  :super ros::object
  :slots (_done ))

(defmethod ros_jetson_stats::fanResponse
  (:init
   (&key
    ((:done __done) "")
    )
   (send-super :init)
   (setq _done (string __done))
   self)
  (:done
   (&optional __done)
   (if __done (setq _done __done)) _done)
  (:serialization-length
   ()
   (+
    ;; string _done
    4 (length _done)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _done
       (write-long (length _done) s) (princ _done s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _done
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _done (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass ros_jetson_stats::fan
  :super ros::object
  :slots ())

(setf (get ros_jetson_stats::fan :md5sum-) "f745cc3cd10b95c8e8f7fabace50fbb1")
(setf (get ros_jetson_stats::fan :datatype-) "ros_jetson_stats/fan")
(setf (get ros_jetson_stats::fan :request) ros_jetson_stats::fanRequest)
(setf (get ros_jetson_stats::fan :response) ros_jetson_stats::fanResponse)

(defmethod ros_jetson_stats::fanRequest
  (:response () (instance ros_jetson_stats::fanResponse :init)))

(setf (get ros_jetson_stats::fanRequest :md5sum-) "f745cc3cd10b95c8e8f7fabace50fbb1")
(setf (get ros_jetson_stats::fanRequest :datatype-) "ros_jetson_stats/fanRequest")
(setf (get ros_jetson_stats::fanRequest :definition-)
      "# fan selection

string mode
int8 fanSpeed
---
string done
")

(setf (get ros_jetson_stats::fanResponse :md5sum-) "f745cc3cd10b95c8e8f7fabace50fbb1")
(setf (get ros_jetson_stats::fanResponse :datatype-) "ros_jetson_stats/fanResponse")
(setf (get ros_jetson_stats::fanResponse :definition-)
      "# fan selection

string mode
int8 fanSpeed
---
string done
")



(provide :ros_jetson_stats/fan "f745cc3cd10b95c8e8f7fabace50fbb1")



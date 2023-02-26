;; Auto-generated. Do not edit!


(when (boundp 'ros_jetson_stats::nvpmodel)
  (if (not (find-package "ROS_JETSON_STATS"))
    (make-package "ROS_JETSON_STATS"))
  (shadow 'nvpmodel (find-package "ROS_JETSON_STATS")))
(unless (find-package "ROS_JETSON_STATS::NVPMODEL")
  (make-package "ROS_JETSON_STATS::NVPMODEL"))
(unless (find-package "ROS_JETSON_STATS::NVPMODELREQUEST")
  (make-package "ROS_JETSON_STATS::NVPMODELREQUEST"))
(unless (find-package "ROS_JETSON_STATS::NVPMODELRESPONSE")
  (make-package "ROS_JETSON_STATS::NVPMODELRESPONSE"))

(in-package "ROS")





(defclass ros_jetson_stats::nvpmodelRequest
  :super ros::object
  :slots (_nvpmodel ))

(defmethod ros_jetson_stats::nvpmodelRequest
  (:init
   (&key
    ((:nvpmodel __nvpmodel) "")
    )
   (send-super :init)
   (setq _nvpmodel (string __nvpmodel))
   self)
  (:nvpmodel
   (&optional __nvpmodel)
   (if __nvpmodel (setq _nvpmodel __nvpmodel)) _nvpmodel)
  (:serialization-length
   ()
   (+
    ;; string _nvpmodel
    4 (length _nvpmodel)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _nvpmodel
       (write-long (length _nvpmodel) s) (princ _nvpmodel s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _nvpmodel
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _nvpmodel (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass ros_jetson_stats::nvpmodelResponse
  :super ros::object
  :slots (_return ))

(defmethod ros_jetson_stats::nvpmodelResponse
  (:init
   (&key
    ((:return __return) "")
    )
   (send-super :init)
   (setq _return (string __return))
   self)
  (:return
   (&optional __return)
   (if __return (setq _return __return)) _return)
  (:serialization-length
   ()
   (+
    ;; string _return
    4 (length _return)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _return
       (write-long (length _return) s) (princ _return s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _return
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _return (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass ros_jetson_stats::nvpmodel
  :super ros::object
  :slots ())

(setf (get ros_jetson_stats::nvpmodel :md5sum-) "7942b12339fc624078e7a634375396ac")
(setf (get ros_jetson_stats::nvpmodel :datatype-) "ros_jetson_stats/nvpmodel")
(setf (get ros_jetson_stats::nvpmodel :request) ros_jetson_stats::nvpmodelRequest)
(setf (get ros_jetson_stats::nvpmodel :response) ros_jetson_stats::nvpmodelResponse)

(defmethod ros_jetson_stats::nvpmodelRequest
  (:response () (instance ros_jetson_stats::nvpmodelResponse :init)))

(setf (get ros_jetson_stats::nvpmodelRequest :md5sum-) "7942b12339fc624078e7a634375396ac")
(setf (get ros_jetson_stats::nvpmodelRequest :datatype-) "ros_jetson_stats/nvpmodelRequest")
(setf (get ros_jetson_stats::nvpmodelRequest :definition-)
      "# NV Power Model selection

string nvpmodel
---
string return
")

(setf (get ros_jetson_stats::nvpmodelResponse :md5sum-) "7942b12339fc624078e7a634375396ac")
(setf (get ros_jetson_stats::nvpmodelResponse :datatype-) "ros_jetson_stats/nvpmodelResponse")
(setf (get ros_jetson_stats::nvpmodelResponse :definition-)
      "# NV Power Model selection

string nvpmodel
---
string return
")



(provide :ros_jetson_stats/nvpmodel "7942b12339fc624078e7a634375396ac")



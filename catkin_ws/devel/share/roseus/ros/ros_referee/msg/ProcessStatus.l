;; Auto-generated. Do not edit!


(when (boundp 'ros_referee::ProcessStatus)
  (if (not (find-package "ROS_REFEREE"))
    (make-package "ROS_REFEREE"))
  (shadow 'ProcessStatus (find-package "ROS_REFEREE")))
(unless (find-package "ROS_REFEREE::PROCESSSTATUS")
  (make-package "ROS_REFEREE::PROCESSSTATUS"))

(in-package "ROS")
;;//! \htmlinclude ProcessStatus.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ros_referee::ProcessStatus
  :super ros::object
  :slots (_header _pid _ppid _cpids _scheduling_policy _priority _imgseq _app _runtime _proposals _objects _probability _data ))

(defmethod ros_referee::ProcessStatus
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:pid __pid) 0)
    ((:ppid __ppid) 0)
    ((:cpids __cpids) (make-array 0 :initial-element 0 :element-type :integer))
    ((:scheduling_policy __scheduling_policy) "")
    ((:priority __priority) 0)
    ((:imgseq __imgseq) 0)
    ((:app __app) "")
    ((:runtime __runtime) 0.0)
    ((:proposals __proposals) 0)
    ((:objects __objects) 0)
    ((:probability __probability) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:data __data) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _header __header)
   (setq _pid (round __pid))
   (setq _ppid (round __ppid))
   (setq _cpids __cpids)
   (setq _scheduling_policy (string __scheduling_policy))
   (setq _priority (round __priority))
   (setq _imgseq (round __imgseq))
   (setq _app (string __app))
   (setq _runtime (float __runtime))
   (setq _proposals (round __proposals))
   (setq _objects (round __objects))
   (setq _probability __probability)
   (setq _data __data)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:pid
   (&optional __pid)
   (if __pid (setq _pid __pid)) _pid)
  (:ppid
   (&optional __ppid)
   (if __ppid (setq _ppid __ppid)) _ppid)
  (:cpids
   (&optional __cpids)
   (if __cpids (setq _cpids __cpids)) _cpids)
  (:scheduling_policy
   (&optional __scheduling_policy)
   (if __scheduling_policy (setq _scheduling_policy __scheduling_policy)) _scheduling_policy)
  (:priority
   (&optional __priority)
   (if __priority (setq _priority __priority)) _priority)
  (:imgseq
   (&optional __imgseq)
   (if __imgseq (setq _imgseq __imgseq)) _imgseq)
  (:app
   (&optional __app)
   (if __app (setq _app __app)) _app)
  (:runtime
   (&optional __runtime)
   (if __runtime (setq _runtime __runtime)) _runtime)
  (:proposals
   (&optional __proposals)
   (if __proposals (setq _proposals __proposals)) _proposals)
  (:objects
   (&optional __objects)
   (if __objects (setq _objects __objects)) _objects)
  (:probability
   (&optional __probability)
   (if __probability (setq _probability __probability)) _probability)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; int64 _pid
    8
    ;; int64 _ppid
    8
    ;; int64[] _cpids
    (* 8    (length _cpids)) 4
    ;; string _scheduling_policy
    4 (length _scheduling_policy)
    ;; uint8 _priority
    1
    ;; int64 _imgseq
    8
    ;; string _app
    4 (length _app)
    ;; float64 _runtime
    8
    ;; int64 _proposals
    8
    ;; int64 _objects
    8
    ;; float64[] _probability
    (* 8    (length _probability)) 4
    ;; int64[] _data
    (* 8    (length _data)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; int64 _pid
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _pid (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _pid) (= (length (_pid . bv)) 2)) ;; bignum
              (write-long (ash (elt (_pid . bv) 0) 0) s)
              (write-long (ash (elt (_pid . bv) 1) -1) s))
             ((and (class _pid) (= (length (_pid . bv)) 1)) ;; big1
              (write-long (elt (_pid . bv) 0) s)
              (write-long (if (>= _pid 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _pid s)(write-long (if (>= _pid 0) 0 #xffffffff) s)))
     ;; int64 _ppid
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _ppid (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _ppid) (= (length (_ppid . bv)) 2)) ;; bignum
              (write-long (ash (elt (_ppid . bv) 0) 0) s)
              (write-long (ash (elt (_ppid . bv) 1) -1) s))
             ((and (class _ppid) (= (length (_ppid . bv)) 1)) ;; big1
              (write-long (elt (_ppid . bv) 0) s)
              (write-long (if (>= _ppid 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _ppid s)(write-long (if (>= _ppid 0) 0 #xffffffff) s)))
     ;; int64[] _cpids
     (write-long (length _cpids) s)
     (dotimes (i (length _cpids))
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke (elt _cpids i) (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class (elt _cpids i)) (= (length ((elt _cpids i) . bv)) 2)) ;; bignum
              (write-long (ash (elt ((elt _cpids i) . bv) 0) 0) s)
              (write-long (ash (elt ((elt _cpids i) . bv) 1) -1) s))
             ((and (class (elt _cpids i)) (= (length ((elt _cpids i) . bv)) 1)) ;; big1
              (write-long (elt ((elt _cpids i) . bv) 0) s)
              (write-long (if (>= (elt _cpids i) 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long (elt _cpids i) s)(write-long (if (>= (elt _cpids i) 0) 0 #xffffffff) s)))
       )
     ;; string _scheduling_policy
       (write-long (length _scheduling_policy) s) (princ _scheduling_policy s)
     ;; uint8 _priority
       (write-byte _priority s)
     ;; int64 _imgseq
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _imgseq (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _imgseq) (= (length (_imgseq . bv)) 2)) ;; bignum
              (write-long (ash (elt (_imgseq . bv) 0) 0) s)
              (write-long (ash (elt (_imgseq . bv) 1) -1) s))
             ((and (class _imgseq) (= (length (_imgseq . bv)) 1)) ;; big1
              (write-long (elt (_imgseq . bv) 0) s)
              (write-long (if (>= _imgseq 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _imgseq s)(write-long (if (>= _imgseq 0) 0 #xffffffff) s)))
     ;; string _app
       (write-long (length _app) s) (princ _app s)
     ;; float64 _runtime
       (sys::poke _runtime (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int64 _proposals
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _proposals (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _proposals) (= (length (_proposals . bv)) 2)) ;; bignum
              (write-long (ash (elt (_proposals . bv) 0) 0) s)
              (write-long (ash (elt (_proposals . bv) 1) -1) s))
             ((and (class _proposals) (= (length (_proposals . bv)) 1)) ;; big1
              (write-long (elt (_proposals . bv) 0) s)
              (write-long (if (>= _proposals 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _proposals s)(write-long (if (>= _proposals 0) 0 #xffffffff) s)))
     ;; int64 _objects
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _objects (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _objects) (= (length (_objects . bv)) 2)) ;; bignum
              (write-long (ash (elt (_objects . bv) 0) 0) s)
              (write-long (ash (elt (_objects . bv) 1) -1) s))
             ((and (class _objects) (= (length (_objects . bv)) 1)) ;; big1
              (write-long (elt (_objects . bv) 0) s)
              (write-long (if (>= _objects 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _objects s)(write-long (if (>= _objects 0) 0 #xffffffff) s)))
     ;; float64[] _probability
     (write-long (length _probability) s)
     (dotimes (i (length _probability))
       (sys::poke (elt _probability i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; int64[] _data
     (write-long (length _data) s)
     (dotimes (i (length _data))
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke (elt _data i) (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class (elt _data i)) (= (length ((elt _data i) . bv)) 2)) ;; bignum
              (write-long (ash (elt ((elt _data i) . bv) 0) 0) s)
              (write-long (ash (elt ((elt _data i) . bv) 1) -1) s))
             ((and (class (elt _data i)) (= (length ((elt _data i) . bv)) 1)) ;; big1
              (write-long (elt ((elt _data i) . bv) 0) s)
              (write-long (if (>= (elt _data i) 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long (elt _data i) s)(write-long (if (>= (elt _data i) 0) 0 #xffffffff) s)))
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; int64 _pid
#+(or :alpha :irix6 :x86_64)
      (setf _pid (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _pid (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; int64 _ppid
#+(or :alpha :irix6 :x86_64)
      (setf _ppid (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _ppid (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; int64[] _cpids
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _cpids (instantiate integer-vector n))
     (dotimes (i n)
#+(or :alpha :irix6 :x86_64)
      (setf (elt _cpids i) (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf (elt _cpids i) (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
     ))
   ;; string _scheduling_policy
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _scheduling_policy (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint8 _priority
     (setq _priority (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; int64 _imgseq
#+(or :alpha :irix6 :x86_64)
      (setf _imgseq (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _imgseq (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; string _app
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _app (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float64 _runtime
     (setq _runtime (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int64 _proposals
#+(or :alpha :irix6 :x86_64)
      (setf _proposals (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _proposals (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; int64 _objects
#+(or :alpha :irix6 :x86_64)
      (setf _objects (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _objects (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; float64[] _probability
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _probability (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _probability i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; int64[] _data
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _data (instantiate integer-vector n))
     (dotimes (i n)
#+(or :alpha :irix6 :x86_64)
      (setf (elt _data i) (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf (elt _data i) (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
     ))
   ;;
   self)
  )

(setf (get ros_referee::ProcessStatus :md5sum-) "60f0fccd1643b5091802875556e45e83")
(setf (get ros_referee::ProcessStatus :datatype-) "ros_referee/ProcessStatus")
(setf (get ros_referee::ProcessStatus :definition-)
      "Header header

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

")



(provide :ros_referee/ProcessStatus "60f0fccd1643b5091802875556e45e83")




(cl:in-package :asdf)

(defsystem "ros_jetson_stats-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "fan" :depends-on ("_package_fan"))
    (:file "_package_fan" :depends-on ("_package"))
    (:file "jetson_clocks" :depends-on ("_package_jetson_clocks"))
    (:file "_package_jetson_clocks" :depends-on ("_package"))
    (:file "nvpmodel" :depends-on ("_package_nvpmodel"))
    (:file "_package_nvpmodel" :depends-on ("_package"))
  ))
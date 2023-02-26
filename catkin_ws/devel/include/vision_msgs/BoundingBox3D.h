// Generated by gencpp from file vision_msgs/BoundingBox3D.msg
// DO NOT EDIT!


#ifndef VISION_MSGS_MESSAGE_BOUNDINGBOX3D_H
#define VISION_MSGS_MESSAGE_BOUNDINGBOX3D_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Vector3.h>

namespace vision_msgs
{
template <class ContainerAllocator>
struct BoundingBox3D_
{
  typedef BoundingBox3D_<ContainerAllocator> Type;

  BoundingBox3D_()
    : center()
    , size()  {
    }
  BoundingBox3D_(const ContainerAllocator& _alloc)
    : center(_alloc)
    , size(_alloc)  {
  (void)_alloc;
    }



   typedef  ::geometry_msgs::Pose_<ContainerAllocator>  _center_type;
  _center_type center;

   typedef  ::geometry_msgs::Vector3_<ContainerAllocator>  _size_type;
  _size_type size;





  typedef boost::shared_ptr< ::vision_msgs::BoundingBox3D_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::vision_msgs::BoundingBox3D_<ContainerAllocator> const> ConstPtr;

}; // struct BoundingBox3D_

typedef ::vision_msgs::BoundingBox3D_<std::allocator<void> > BoundingBox3D;

typedef boost::shared_ptr< ::vision_msgs::BoundingBox3D > BoundingBox3DPtr;
typedef boost::shared_ptr< ::vision_msgs::BoundingBox3D const> BoundingBox3DConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::vision_msgs::BoundingBox3D_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::vision_msgs::BoundingBox3D_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::vision_msgs::BoundingBox3D_<ContainerAllocator1> & lhs, const ::vision_msgs::BoundingBox3D_<ContainerAllocator2> & rhs)
{
  return lhs.center == rhs.center &&
    lhs.size == rhs.size;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::vision_msgs::BoundingBox3D_<ContainerAllocator1> & lhs, const ::vision_msgs::BoundingBox3D_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace vision_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::vision_msgs::BoundingBox3D_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::vision_msgs::BoundingBox3D_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::vision_msgs::BoundingBox3D_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::vision_msgs::BoundingBox3D_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::vision_msgs::BoundingBox3D_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::vision_msgs::BoundingBox3D_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::vision_msgs::BoundingBox3D_<ContainerAllocator> >
{
  static const char* value()
  {
    return "727c83f2b037373b8e968433d9c84ecb";
  }

  static const char* value(const ::vision_msgs::BoundingBox3D_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x727c83f2b037373bULL;
  static const uint64_t static_value2 = 0x8e968433d9c84ecbULL;
};

template<class ContainerAllocator>
struct DataType< ::vision_msgs::BoundingBox3D_<ContainerAllocator> >
{
  static const char* value()
  {
    return "vision_msgs/BoundingBox3D";
  }

  static const char* value(const ::vision_msgs::BoundingBox3D_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::vision_msgs::BoundingBox3D_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# A 3D bounding box that can be positioned and rotated about its center (6 DOF)\n"
"# Dimensions of this box are in meters, and as such, it may be migrated to\n"
"#   another package, such as geometry_msgs, in the future.\n"
"\n"
"# The 3D position and orientation of the bounding box center\n"
"geometry_msgs/Pose center\n"
"\n"
"# The size of the bounding box, in meters, surrounding the object's center\n"
"#   pose.\n"
"geometry_msgs/Vector3 size\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Pose\n"
"# A representation of pose in free space, composed of position and orientation. \n"
"Point position\n"
"Quaternion orientation\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Point\n"
"# This contains the position of a point in free space\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Quaternion\n"
"# This represents an orientation in free space in quaternion form.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"float64 w\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Vector3\n"
"# This represents a vector in free space. \n"
"# It is only meant to represent a direction. Therefore, it does not\n"
"# make sense to apply a translation to it (e.g., when applying a \n"
"# generic rigid transformation to a Vector3, tf2 will only apply the\n"
"# rotation). If you want your data to be translatable too, use the\n"
"# geometry_msgs/Point message instead.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
;
  }

  static const char* value(const ::vision_msgs::BoundingBox3D_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::vision_msgs::BoundingBox3D_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.center);
      stream.next(m.size);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct BoundingBox3D_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::vision_msgs::BoundingBox3D_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::vision_msgs::BoundingBox3D_<ContainerAllocator>& v)
  {
    s << indent << "center: ";
    s << std::endl;
    Printer< ::geometry_msgs::Pose_<ContainerAllocator> >::stream(s, indent + "  ", v.center);
    s << indent << "size: ";
    s << std::endl;
    Printer< ::geometry_msgs::Vector3_<ContainerAllocator> >::stream(s, indent + "  ", v.size);
  }
};

} // namespace message_operations
} // namespace ros

#endif // VISION_MSGS_MESSAGE_BOUNDINGBOX3D_H

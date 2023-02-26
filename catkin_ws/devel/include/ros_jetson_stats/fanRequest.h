// Generated by gencpp from file ros_jetson_stats/fanRequest.msg
// DO NOT EDIT!


#ifndef ROS_JETSON_STATS_MESSAGE_FANREQUEST_H
#define ROS_JETSON_STATS_MESSAGE_FANREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace ros_jetson_stats
{
template <class ContainerAllocator>
struct fanRequest_
{
  typedef fanRequest_<ContainerAllocator> Type;

  fanRequest_()
    : mode()
    , fanSpeed(0)  {
    }
  fanRequest_(const ContainerAllocator& _alloc)
    : mode(_alloc)
    , fanSpeed(0)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _mode_type;
  _mode_type mode;

   typedef int8_t _fanSpeed_type;
  _fanSpeed_type fanSpeed;





  typedef boost::shared_ptr< ::ros_jetson_stats::fanRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ros_jetson_stats::fanRequest_<ContainerAllocator> const> ConstPtr;

}; // struct fanRequest_

typedef ::ros_jetson_stats::fanRequest_<std::allocator<void> > fanRequest;

typedef boost::shared_ptr< ::ros_jetson_stats::fanRequest > fanRequestPtr;
typedef boost::shared_ptr< ::ros_jetson_stats::fanRequest const> fanRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ros_jetson_stats::fanRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ros_jetson_stats::fanRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::ros_jetson_stats::fanRequest_<ContainerAllocator1> & lhs, const ::ros_jetson_stats::fanRequest_<ContainerAllocator2> & rhs)
{
  return lhs.mode == rhs.mode &&
    lhs.fanSpeed == rhs.fanSpeed;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::ros_jetson_stats::fanRequest_<ContainerAllocator1> & lhs, const ::ros_jetson_stats::fanRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace ros_jetson_stats

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::ros_jetson_stats::fanRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ros_jetson_stats::fanRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ros_jetson_stats::fanRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ros_jetson_stats::fanRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_jetson_stats::fanRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_jetson_stats::fanRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ros_jetson_stats::fanRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a40184a9984237fb3cdc8207761a7cfe";
  }

  static const char* value(const ::ros_jetson_stats::fanRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa40184a9984237fbULL;
  static const uint64_t static_value2 = 0x3cdc8207761a7cfeULL;
};

template<class ContainerAllocator>
struct DataType< ::ros_jetson_stats::fanRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ros_jetson_stats/fanRequest";
  }

  static const char* value(const ::ros_jetson_stats::fanRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ros_jetson_stats::fanRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# fan selection\n"
"\n"
"string mode\n"
"int8 fanSpeed\n"
;
  }

  static const char* value(const ::ros_jetson_stats::fanRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ros_jetson_stats::fanRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.mode);
      stream.next(m.fanSpeed);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct fanRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ros_jetson_stats::fanRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ros_jetson_stats::fanRequest_<ContainerAllocator>& v)
  {
    s << indent << "mode: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.mode);
    s << indent << "fanSpeed: ";
    Printer<int8_t>::stream(s, indent + "  ", v.fanSpeed);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ROS_JETSON_STATS_MESSAGE_FANREQUEST_H

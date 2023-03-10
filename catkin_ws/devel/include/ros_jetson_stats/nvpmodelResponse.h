// Generated by gencpp from file ros_jetson_stats/nvpmodelResponse.msg
// DO NOT EDIT!


#ifndef ROS_JETSON_STATS_MESSAGE_NVPMODELRESPONSE_H
#define ROS_JETSON_STATS_MESSAGE_NVPMODELRESPONSE_H


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
struct nvpmodelResponse_
{
  typedef nvpmodelResponse_<ContainerAllocator> Type;

  nvpmodelResponse_()
    : return()  {
    }
  nvpmodelResponse_(const ContainerAllocator& _alloc)
    : return(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _return_type;
  _return_type return;





  typedef boost::shared_ptr< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> const> ConstPtr;

}; // struct nvpmodelResponse_

typedef ::ros_jetson_stats::nvpmodelResponse_<std::allocator<void> > nvpmodelResponse;

typedef boost::shared_ptr< ::ros_jetson_stats::nvpmodelResponse > nvpmodelResponsePtr;
typedef boost::shared_ptr< ::ros_jetson_stats::nvpmodelResponse const> nvpmodelResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator1> & lhs, const ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator2> & rhs)
{
  return lhs.return == rhs.return;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator1> & lhs, const ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace ros_jetson_stats

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "8d02df2c0dff1a16a80230979e550820";
  }

  static const char* value(const ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x8d02df2c0dff1a16ULL;
  static const uint64_t static_value2 = 0xa80230979e550820ULL;
};

template<class ContainerAllocator>
struct DataType< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ros_jetson_stats/nvpmodelResponse";
  }

  static const char* value(const ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string return\n"
;
  }

  static const char* value(const ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.return);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct nvpmodelResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ros_jetson_stats::nvpmodelResponse_<ContainerAllocator>& v)
  {
    s << indent << "return: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.return);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ROS_JETSON_STATS_MESSAGE_NVPMODELRESPONSE_H

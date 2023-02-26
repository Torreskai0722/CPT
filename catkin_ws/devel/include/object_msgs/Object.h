// Generated by gencpp from file object_msgs/Object.msg
// DO NOT EDIT!


#ifndef OBJECT_MSGS_MESSAGE_OBJECT_H
#define OBJECT_MSGS_MESSAGE_OBJECT_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace object_msgs
{
template <class ContainerAllocator>
struct Object_
{
  typedef Object_<ContainerAllocator> Type;

  Object_()
    : object_name()
    , probability(0.0)  {
    }
  Object_(const ContainerAllocator& _alloc)
    : object_name(_alloc)
    , probability(0.0)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _object_name_type;
  _object_name_type object_name;

   typedef float _probability_type;
  _probability_type probability;





  typedef boost::shared_ptr< ::object_msgs::Object_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::object_msgs::Object_<ContainerAllocator> const> ConstPtr;

}; // struct Object_

typedef ::object_msgs::Object_<std::allocator<void> > Object;

typedef boost::shared_ptr< ::object_msgs::Object > ObjectPtr;
typedef boost::shared_ptr< ::object_msgs::Object const> ObjectConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::object_msgs::Object_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::object_msgs::Object_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::object_msgs::Object_<ContainerAllocator1> & lhs, const ::object_msgs::Object_<ContainerAllocator2> & rhs)
{
  return lhs.object_name == rhs.object_name &&
    lhs.probability == rhs.probability;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::object_msgs::Object_<ContainerAllocator1> & lhs, const ::object_msgs::Object_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace object_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::object_msgs::Object_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::object_msgs::Object_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::object_msgs::Object_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::object_msgs::Object_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::object_msgs::Object_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::object_msgs::Object_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::object_msgs::Object_<ContainerAllocator> >
{
  static const char* value()
  {
    return "b62386628eb32e68aec0dfe4b39247d3";
  }

  static const char* value(const ::object_msgs::Object_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xb62386628eb32e68ULL;
  static const uint64_t static_value2 = 0xaec0dfe4b39247d3ULL;
};

template<class ContainerAllocator>
struct DataType< ::object_msgs::Object_<ContainerAllocator> >
{
  static const char* value()
  {
    return "object_msgs/Object";
  }

  static const char* value(const ::object_msgs::Object_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::object_msgs::Object_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# Copyright (c) 2017 Intel Corporation\n"
"#\n"
"# Licensed under the Apache License, Version 2.0 (the \"License\");\n"
"# you may not use this file except in compliance with the License.\n"
"# You may obtain a copy of the License at\n"
"#\n"
"#      http://www.apache.org/licenses/LICENSE-2.0\n"
"#\n"
"# Unless required by applicable law or agreed to in writing, software\n"
"# distributed under the License is distributed on an \"AS IS\" BASIS,\n"
"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
"# See the License for the specific language governing permissions and\n"
"# limitations under the License.\n"
"\n"
"# This message define the property of detected object\n"
"string object_name  # object name\n"
"float32 probability # probability of detected object\n"
;
  }

  static const char* value(const ::object_msgs::Object_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::object_msgs::Object_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.object_name);
      stream.next(m.probability);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Object_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::object_msgs::Object_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::object_msgs::Object_<ContainerAllocator>& v)
  {
    s << indent << "object_name: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.object_name);
    s << indent << "probability: ";
    Printer<float>::stream(s, indent + "  ", v.probability);
  }
};

} // namespace message_operations
} // namespace ros

#endif // OBJECT_MSGS_MESSAGE_OBJECT_H

// Generated by gencpp from file ros_jetson_stats/nvpmodel.msg
// DO NOT EDIT!


#ifndef ROS_JETSON_STATS_MESSAGE_NVPMODEL_H
#define ROS_JETSON_STATS_MESSAGE_NVPMODEL_H

#include <ros/service_traits.h>


#include <ros_jetson_stats/nvpmodelRequest.h>
#include <ros_jetson_stats/nvpmodelResponse.h>


namespace ros_jetson_stats
{

struct nvpmodel
{

typedef nvpmodelRequest Request;
typedef nvpmodelResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct nvpmodel
} // namespace ros_jetson_stats


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::ros_jetson_stats::nvpmodel > {
  static const char* value()
  {
    return "7942b12339fc624078e7a634375396ac";
  }

  static const char* value(const ::ros_jetson_stats::nvpmodel&) { return value(); }
};

template<>
struct DataType< ::ros_jetson_stats::nvpmodel > {
  static const char* value()
  {
    return "ros_jetson_stats/nvpmodel";
  }

  static const char* value(const ::ros_jetson_stats::nvpmodel&) { return value(); }
};


// service_traits::MD5Sum< ::ros_jetson_stats::nvpmodelRequest> should match
// service_traits::MD5Sum< ::ros_jetson_stats::nvpmodel >
template<>
struct MD5Sum< ::ros_jetson_stats::nvpmodelRequest>
{
  static const char* value()
  {
    return MD5Sum< ::ros_jetson_stats::nvpmodel >::value();
  }
  static const char* value(const ::ros_jetson_stats::nvpmodelRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::ros_jetson_stats::nvpmodelRequest> should match
// service_traits::DataType< ::ros_jetson_stats::nvpmodel >
template<>
struct DataType< ::ros_jetson_stats::nvpmodelRequest>
{
  static const char* value()
  {
    return DataType< ::ros_jetson_stats::nvpmodel >::value();
  }
  static const char* value(const ::ros_jetson_stats::nvpmodelRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::ros_jetson_stats::nvpmodelResponse> should match
// service_traits::MD5Sum< ::ros_jetson_stats::nvpmodel >
template<>
struct MD5Sum< ::ros_jetson_stats::nvpmodelResponse>
{
  static const char* value()
  {
    return MD5Sum< ::ros_jetson_stats::nvpmodel >::value();
  }
  static const char* value(const ::ros_jetson_stats::nvpmodelResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::ros_jetson_stats::nvpmodelResponse> should match
// service_traits::DataType< ::ros_jetson_stats::nvpmodel >
template<>
struct DataType< ::ros_jetson_stats::nvpmodelResponse>
{
  static const char* value()
  {
    return DataType< ::ros_jetson_stats::nvpmodel >::value();
  }
  static const char* value(const ::ros_jetson_stats::nvpmodelResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // ROS_JETSON_STATS_MESSAGE_NVPMODEL_H

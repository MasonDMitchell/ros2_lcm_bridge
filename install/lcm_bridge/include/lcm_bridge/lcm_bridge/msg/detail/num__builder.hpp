// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from lcm_bridge:msg/Num.idl
// generated code does not contain a copyright notice

#ifndef LCM_BRIDGE__MSG__DETAIL__NUM__BUILDER_HPP_
#define LCM_BRIDGE__MSG__DETAIL__NUM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "lcm_bridge/msg/detail/num__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace lcm_bridge
{

namespace msg
{

namespace builder
{

class Init_Num_num
{
public:
  Init_Num_num()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::lcm_bridge::msg::Num num(::lcm_bridge::msg::Num::_num_type arg)
  {
    msg_.num = std::move(arg);
    return std::move(msg_);
  }

private:
  ::lcm_bridge::msg::Num msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::lcm_bridge::msg::Num>()
{
  return lcm_bridge::msg::builder::Init_Num_num();
}

}  // namespace lcm_bridge

#endif  // LCM_BRIDGE__MSG__DETAIL__NUM__BUILDER_HPP_

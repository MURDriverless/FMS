#ifndef LIDAR_ANALYZER_H
#define LIDAR_ANALYZER_H

#include <diagnostic_aggregator/generic_analyzer.h>
#include <std_msgs/Int8.h>
#include <mur_common/status_msg.h>

namespace diagnostic_aggregator {

class LidarAnalyzer : public GenericAnalyzer {
 public:
  LidarAnalyzer();
  virtual bool init(const std::string base_path, const ros::NodeHandle &n);
  virtual std::vector<diagnostic_msgs::DiagnosticStatusPtr> report();

 private:
  int8_t level_;
  ros::Publisher status_publisher_;
};

}  // namespace diagnostic_aggregator

#endif  // LIDAR_ANALYZER_H

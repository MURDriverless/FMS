#ifndef GPS_ANALYZER_H
#define GPS_ANALYZER_H

#include <diagnostic_aggregator/generic_analyzer.h>
#include <std_msgs/Int8.h>
#include <mur_common/status_msg.h>

namespace diagnostic_aggregator {

class GPSAnalyzer : public GenericAnalyzer {
 public:
  GPSAnalyzer();
  virtual bool init(const std::string base_path, const ros::NodeHandle &n);
  virtual std::vector<diagnostic_msgs::DiagnosticStatusPtr> report();

 private:
  int8_t level_;
  ros::Publisher status_publisher_;
};

}  // namespace diagnostic_aggregator

#endif  // GPS_ANALYZER_H

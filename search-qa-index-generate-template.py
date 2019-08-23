import string
import os
import sys

class PartitionFormatter(string.Formatter):
    def format_field(self, value, spec):
        if spec.startswith('repeat'):
            template = spec.partition(':')[-1]
            if type(value) is dict:
                value = value.items()
            return ''.join([template.format(partitionId=item) for item in value])
        else:
            return super(SuperFormatter, self).format_field(value, spec)

current_dir = os.path.dirname(os.path.abspath(__file__))
template_file_name = os.path.join(current_dir, './search-qa-index.template.yaml')
output_file_name = os.path.join(current_dir, './search-qa-index.generated.yaml')

num_partitions = int(sys.argv[1])
partitions = range(1, num_partitions + 1)

partition_formatter = PartitionFormatter()
with open(template_file_name, 'r') as template_file:
    template = template_file.read()
    cf_template = partition_formatter.format(template, partitions=partitions)
    with open(output_file_name, 'w') as output_file:
        output_file.write(cf_template)
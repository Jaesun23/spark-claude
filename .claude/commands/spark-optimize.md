# /spark-optimize - SPARK Performance Optimization Pipeline

**Purpose**: Comprehensive performance optimization with analysis, implementation, and validation

## Execution Instructions

When this command is called, execute the following performance optimization pipeline:

```
1. First, use the Task tool with subagent_type "analyzer-spark" to identify performance bottlenecks.
   Pass "Conduct comprehensive performance analysis: identify bottlenecks, memory leaks, slow queries, and optimization opportunities" as the prompt.

2. After analysis, use the Task tool with subagent_type "troubleshooter-spark"  
   to investigate root causes of performance issues.
   Pass "Investigate performance issues identified in analysis: profile code, trace bottlenecks, and determine optimization strategies" as the prompt.

3. Then, use the Task tool with subagent_type "improver-spark"
   to implement performance optimizations.
   Pass "Implement performance optimizations: optimize algorithms, improve queries, enhance caching, and refactor inefficient code" as the prompt.

4. Next, use the Task tool with subagent_type "tester-spark"
   to create performance benchmarks and validation tests.
   Pass "Create comprehensive performance tests: benchmarks, load tests, stress tests, and regression prevention tests" as the prompt.

5. Finally, use the Task tool with subagent_type "documenter-spark"
   to document optimizations and create monitoring guides.
   Pass "Document performance improvements: optimization techniques used, benchmark results, and monitoring recommendations" as the prompt.
```

## Usage Examples

```bash
/spark-optimize "optimize API response times and database query performance"
/spark-optimize "improve frontend loading speed and bundle size optimization"
/spark-optimize "optimize memory usage and garbage collection in data processing"  
/spark-optimize "enhance search functionality performance with indexing strategies"
/spark-optimize "optimize image processing pipeline for faster throughput"
```

## Optimization Areas

- **Application Performance**: Algorithm optimization, caching strategies, code efficiency
- **Database Performance**: Query optimization, indexing, connection pooling
- **Frontend Performance**: Bundle optimization, lazy loading, rendering improvements
- **Infrastructure Performance**: Memory management, CPU utilization, I/O optimization
- **Network Performance**: Request optimization, compression, CDN utilization

## Performance Metrics

- ⚡ **Response Time**: Latency improvements and throughput increases
- 💾 **Memory Usage**: Memory leak fixes and usage optimization  
- 🗄️ **Database Performance**: Query speed and connection efficiency
- 📦 **Bundle Size**: Frontend optimization and loading improvements
- 🔄 **Scalability**: Performance under load and concurrent usage

## Expected Deliverables

1. **Performance Analysis**: Detailed bottleneck identification and metrics
2. **Root Cause Investigation**: Deep dive into performance issue sources
3. **Optimized Implementation**: Improved code with performance enhancements
4. **Benchmark Suite**: Comprehensive performance testing and monitoring
5. **Optimization Guide**: Documentation of improvements and monitoring setup

## SPARK Intelligence Integration

- 🔍 **5-Agent Pipeline**: Specialized performance expertise at each stage
- 📊 **Data-Driven**: All optimizations backed by metrics and benchmarks
- 🧪 **Validation-First**: Comprehensive testing ensures improvements work
- 📚 **Knowledge Transfer**: Complete documentation for team learning
- 🚀 **88.4% Token Efficiency**: Complex optimization without token overhead
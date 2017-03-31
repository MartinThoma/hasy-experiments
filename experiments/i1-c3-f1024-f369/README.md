Evaluate model
i1-c3-f1024-f369:
    train_time:    2207.3 (min=2089.73, max=2719.93)
    test_time:    2.1 (min=2.01, max=2.26)
    acc:        72.7 (min=71.9, max=73.2)
{'i1-c3-f1024-f369': [{'training_time': 2089.7255911827087, 'testing_time': 2.075740098953247, 'accuracy': 0.7275188323917138}, {'training_time': 2089.747293949127, 'testing_time': 2.007943868637085, 'accuracy': 0.7321333726763057}, {'training_time': 2152.6032330989838, 'testing_time': 2.2629480361938477, 'accuracy': 0.7280198663749778}, {'training_time': 2719.9316821098328, 'testing_time': 2.0160138607025146, 'accuracy': 0.7286518518518519}, {'training_time': 2098.034945011139, 'testing_time': 2.082184076309204, 'accuracy': 0.7187908302648771}, {'training_time': 2093.558618068695, 'testing_time': 2.0698421001434326, 'accuracy': 0.7261748958953004}]}
I tensorflow/core/common_runtime/gpu/gpu_device.cc:975] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GeForce 940MX, pci bus id: 0000:02:00.0)
    shape: (3, 3, 1, 3)
    variable_parametes: 27
    ---
    shape: (3,)
    variable_parametes: 3
    ---
    shape: (3072, 1024)
    variable_parametes: 3145728
    ---
    shape: (1024,)
    variable_parametes: 1024
    ---
    shape: (1024, 369)
    variable_parametes: 377856
    ---
    shape: (369,)
    variable_parametes: 369
    ---
total_parameters: 3525007
model_checkpoint_path: checkpoints/hasy_i1-c3-f1024-f369_model.ckpt
validation_curve_path: validation-curve-accuracy-i1-c3-f1024-f369-6.csv
^CTraceback (most recent call last):
  File "tf_hasy.py", line 146, in <module>
    y_: batch[1]
  File "/usr/local/lib/python2.7/dist-packages/tensorflow/python/framework/ops.py", line 1588, in run
    _run_using_default_session(self, feed_dict, self.graph, session)
  File "/usr/local/lib/python2.7/dist-packages/tensorflow/python/framework/ops.py", line 3832, in _run_using_default_session
    session.run(operation, feed_dict)
  File "/usr/local/lib/python2.7/dist-packages/tensorflow/python/client/session.py", line 767, in run
    run_metadata_ptr)
  File "/usr/local/lib/python2.7/dist-packages/tensorflow/python/client/session.py", line 965, in _run
    feed_dict_string, options, run_metadata)
  File "/usr/local/lib/python2.7/dist-packages/tensorflow/python/client/session.py", line 1015, in _do_run
    target_list, options, run_metadata)
  File "/usr/local/lib/python2.7/dist-packages/tensorflow/python/client/session.py", line 1022, in _do_call
    return fn(*args)
  File "/usr/local/lib/python2.7/dist-packages/tensorflow/python/client/session.py", line 1004, in _run_fn
    status, run_metadata)
KeyboardInterrupt

real    14397,24s
user    11355,81s
sys    2556,92s
/*
 * Copyright (c) 2005, 2009 The Australian National University.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Apache License v2.0.
 * You may obtain the license at
 * 
 *    http://www.opensource.org/licenses/apache2.0.php
 */
package org.dacapo.harness;

import java.io.File;
import java.lang.reflect.Constructor;

import org.dacapo.parser.Config;

/**
 * date:  $Date: 2009-12-24 11:19:36 +1100 (Thu, 24 Dec 2009) $
 * id: $Id: Lusearch.java 738 2009-12-24 00:19:36Z steveb-oss $
 */
public class Lusearch extends org.dacapo.harness.Benchmark {
  private final Object benchmark;

  public Lusearch(Config config, File scratch, File data) throws Exception {
    super(config, scratch, data, false);
    Class<?> clazz = Class.forName("org.dacapo.lusearch.Search", true, loader);
    this.method = clazz.getMethod("main", String[].class);
    Constructor<?> cons = clazz.getConstructor(org.dacapo.harness.Callback.class);
    useBenchmarkClassLoader();
    try {
      if (Benchmark.callback == null) {
        System.out.println("callback is null");
        System.exit(100);
      }
      benchmark = cons.newInstance(Benchmark.callback);
    } finally {
      revertClassLoader();
    }
  }

  @Override
  public void iterate(String size) throws Exception {
    method.invoke(benchmark, (Object) (config.preprocessArgs(size, scratch, data)));
  }
}

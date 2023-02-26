# -*- coding: utf-8 -*-
"""
    Module with CPUFreq class that manage the CPU frequency.
"""
from os import path
import sys
import os
import socket
import yaml
import pickle
import time
import threading

class CPUFreqBaseError(Exception):
    """Base Exception raised for errors in the Class CPUFreq."""
    pass


class CPUFreqErrorInit(CPUFreqBaseError):
    """Exception raised for errors at initializing of CPUFreq Class.
    Attributes:
        expression - input expression in which the error occurred
        message - explanation of the error
    """

    def __init__(self, message):
        self.message = message


class cpuFreq:
    """
    Class that manage cpus frequencies
        Attributes
            sock
            driver
            available_governors
            available_frequencies
        Methods
            enable_all_cpu()
            reset()
            disable_hyperthread()
            disable_cpu()
            enable_cpu()
            set_frequencies()
            set_min_frequencies()
            set_max_frequencies()
            set_governors()
            get_online_cpus()
            get_governors()
            get_frequencies()
    """

    BASEDIR = "/sys/devices/system/cpu"
    __instance = None
    SOCK_PATH = "/tmp/cpufreq_manager"
    PORT = 65500

    # def __new__(cls, *args, **kwargs):
    #     if cpuFreq.__instance == None:
    #         LINUX = sys.platform.startswith("linux")
    #         DRIVERFREQ = path.isfile(path.join(cpuFreq.BASEDIR,
    #                                            "cpu0",
    #                                            "cpufreq",
    #                                            "scaling_driver"))
    #         if not LINUX:
    #             raise CPUFreqErrorInit("ERROR: %s Class should be used only "
    #                                    "on Linux Systems." % cls.__name__)
    #         elif not DRIVERFREQ:
    #             raise CPUFreqErrorInit("ERROR: %s Class should be used only "
    #                                    "with OS CPU Power driver activated (Linux ACPI "
    #                                    "module, for example)." % cls.__name__)
    #         else:
    #             cpuFreq.__instance = super().__new__(cls)
    #             fpath = path.join("cpu0", "cpufreq", "scaling_driver")
    #             datad = cpuFreq.__instance.__read_cpu_file(fpath)
    #             datad = datad.rstrip("\n").split()[0]

    #             fpath = path.join("cpu0", "cpufreq",
    #                               "scaling_available_governors")
    #             datag = cpuFreq.__instance.__read_cpu_file(fpath)
    #             datag = datag.rstrip("\n").split()

    #             fpath = path.join("cpu0", "cpufreq",
    #                               "scaling_available_frequencies")
    #             dataf = cpuFreq.__instance.__read_cpu_file(fpath)
    #             dataf = dataf.rstrip("\n").split()

    #             cpuFreq.__instance.driver = datad
    #             cpuFreq.__instance.available_governors = datag
    #             cpuFreq.__instance.available_frequencies = list(
    #                 map(int, dataf))
                
    #             # cpuFreq.__instance.sock = socket.socket(socket.AF_UNIX)
    #             # try:
    #             #     os.unlink(cpuFreq.SOCK_PATH)
    #             # except:
    #             #     pass
    #             # cpuFreq.__instance.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #             # cpuFreq.__instance.sock.bind(cpuFreq.SOCK_PATH)
    #             # cpuFreq.__instance.sock.listen(cpuFreq.PORT)
    #             # os.chmod(cpuFreq.SOCK_PATH, 0o777)

    #     return cpuFreq.__instance
    
    def __init__(self):
        LINUX = sys.platform.startswith("linux")
        DRIVERFREQ = path.isfile(path.join(cpuFreq.BASEDIR,
                                            "cpu0",
                                            "cpufreq",
                                            "scaling_driver"))
        if not LINUX:
            raise CPUFreqErrorInit("ERROR: %s Class should be used only "
                                    "on Linux Systems." % cls.__name__)
        elif not DRIVERFREQ:
            raise CPUFreqErrorInit("ERROR: %s Class should be used only "
                                    "with OS CPU Power driver activated (Linux ACPI "
                                    "module, for example)." % cls.__name__)
        
        fpath = path.join("cpu0", "cpufreq", "scaling_driver")
        datad = self.__read_cpu_file(fpath)
        datad = datad.rstrip("\n").split()[0]

        fpath = path.join("cpu0", "cpufreq",
                            "scaling_available_governors")
        datag = self.__read_cpu_file(fpath)
        datag = datag.rstrip("\n").split()

        fpath = path.join("cpu0", "cpufreq",
                            "scaling_available_frequencies")
        dataf = self.__read_cpu_file(fpath)
        dataf = dataf.rstrip("\n").split()

        self.driver = datad
        self.available_governors = datag
        self.available_frequencies = list(map(int, dataf))

        self.sock = socket.socket(socket.AF_UNIX)
        try:
            os.unlink(cpuFreq.SOCK_PATH)
        except:
            pass
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(cpuFreq.SOCK_PATH)
        self.sock.listen(cpuFreq.PORT)
        os.chmod(cpuFreq.SOCK_PATH, 0o777)

    # private
    def __read_cpu_file(self, fname):
        fpath = path.join(cpuFreq.BASEDIR, fname)
        with open(fpath, "rb") as f:
            data = f.read().decode("utf-8")
        return data

    def __write_cpu_file(self, fname, data):
        fpath = path.join(cpuFreq.BASEDIR, fname)
        with open(fpath, "wb") as f:
            f.write(data)

    def __get_cpu_variable(self, var):
        data = {}
        for cpu in self.__get_ranges("online"):
            fpath = path.join("cpu%i" % cpu, "cpufreq", var)
            data[int(cpu)] = self.__read_cpu_file(
                fpath).rstrip("\n").split()[0]
        return data

    def __get_ranges(self, fname):
        str_range = self.__read_cpu_file(fname).strip("\n").strip()
        l = []
        if not str_range:
            return l
        for r in str_range.split(","):
            mr = r.split("-")
            if len(mr) == 2:
                l += list(range(int(mr[0]),  int(mr[1])+1))
            else:
                l += [int(mr[0])]
        return l

    # interfaces
    def enable_all_cpu(self):
        """
        Enable all offline cpus
        """
        to_enable = set(self.__get_ranges("present"))
        to_enable = to_enable & set(self.__get_ranges("offline"))
        for cpu in to_enable:
            fpath = path.join("cpu%i" % cpu, "online")
            self.__write_cpu_file(fpath, b"1")

    def reset(self, rg=None):
        """
        Enable all offline cpus, and reset max and min frequencies files

        rg: range or list of threads to reset
        """
        if isinstance(rg, int):
            rg = [rg]
        to_reset = rg if rg else self.__get_ranges("present")
        self.enable_cpu(to_reset)
        self.set_governors("ondemand", rg=rg)
        for cpu in to_reset:
            fpath = path.join("cpu%i" % cpu, "cpufreq", "scaling_max_freq")
            max_f = str(max(self.available_frequencies)).encode()
            self.__write_cpu_file(fpath, max_f)
            fpath = path.join("cpu%i" % cpu, "cpufreq", "scaling_min_freq")
            min_f = str(min(self.available_frequencies)).encode()
            self.__write_cpu_file(fpath, min_f)
        
        return True

    def disable_hyperthread(self):
        """
        Disable all threads attached to the same core
        """
        to_disable = []
        online_cpus = self.__get_ranges("online")
        for cpu in online_cpus:
            fpath = path.join("cpu%i" % cpu, "topology",
                              "thread_siblings_list")
            to_disable += self.__get_ranges(fpath)[1:]
        to_disable = set(to_disable) & set(online_cpus)

        for cpu in to_disable:
            fpath = path.join("cpu%i" % cpu, "online")
            self.__write_cpu_file(fpath, b"0")
        
        return True

    def disable_cpu(self, rg):
        """
        Disable cpus

        rg: range or list of threads to disable
        """
        if isinstance(rg, int):
            rg = [rg]
        to_disable = set(rg) & set(self.__get_ranges("online"))
        for cpu in to_disable:
            fpath = path.join("cpu%i" % cpu, "online")
            self.__write_cpu_file(fpath, b"0")
        
        return True

    def enable_cpu(self, rg):
        """
        Enable cpus

        rg: range or list of threads to enable
        """
        if isinstance(rg, int):
            rg = [rg]
        to_disable = set(rg) & set(self.__get_ranges("offline"))
        for cpu in to_disable:
            fpath = path.join("cpu%i" % cpu, "online")
            self.__write_cpu_file(fpath, b"1")
        
        return True

    def set_frequencies(self, freq, rg=None):
        """
        Set cores frequencies

        freq: int frequency in KHz
        rg: list of range of cores
        """
        # print(freq)

        if not isinstance(freq, int):
            raise CPUFreqBaseError(
                "ERROR: Frequency should be a Integer value")
        to_change = self.__get_ranges("online")
        if isinstance(rg, int):
            rg = [rg]
        if rg:
            to_change = set(rg) & set(self.__get_ranges("online"))
        max_freqs = self.get_max_freq()
        min_freqs = self.get_min_freq()
        # print(to_change)
        for cpu in to_change:
            fpath = path.join("cpu%i" % cpu, "cpufreq", "scaling_setspeed")
            try:
                self.__write_cpu_file(fpath, str(freq).encode())
            except Exception as e:
                print(e, freq, "{} - {}.".format(min_freqs[cpu], max_freqs[cpu]))
                raise CPUFreqBaseError(("ERROR: Frequency should be between"
                                        "min and max frequencies interval: "
                                        "{} - {}.".format(min_freqs[cpu], max_freqs[cpu])))
        
        return True

    def set_max_frequencies(self, freq, rg=None):
        """
        Set cores max frequencies

        freq: int frequency in KHz
        rg: list of range of cores
        """

        if not isinstance(freq, int):
            raise CPUFreqBaseError(
                "ERROR: Frequency should be a Integer value")
        to_change = self.__get_ranges("online")
        if isinstance(rg, int):
            rg = [rg]
        if rg:
            to_change = set(rg) & set(self.__get_ranges("online"))
        min_freqs = self.get_min_freq()
        for cpu in to_change:
            fpath = path.join("cpu%i" % cpu, "cpufreq", "scaling_max_freq")
            try:
                self.__write_cpu_file(fpath, str(freq).encode())
            except Exception as e:
                print(e, freq, "{}".format(min_freqs[cpu]))
                raise CPUFreqBaseError(("ERROR: Frequency should be gt min "
                                        "freq: {}".format(min_freqs[cpu])))
        
        return True

    def set_min_frequencies(self, freq, rg=None):
        """
        Set cores min frequencies

        freq: int frequency in KHz
        rg: list of range of cores
        """
        if not isinstance(freq, int):
            raise CPUFreqBaseError(
                "ERROR: Frequency should be a Integer value")
        to_change = self.__get_ranges("online")
        if isinstance(rg, int):
            rg = [rg]
        if rg:
            to_change = set(rg) & set(self.__get_ranges("online"))
        max_freqs = self.get_max_freq()
        for cpu in to_change:
            fpath = path.join("cpu%i" % cpu, "cpufreq", "scaling_min_freq")
            try:
                self.__write_cpu_file(fpath, str(freq).encode())
            except Exception as e:
                print(e, freq, "{}.".format(max_freqs[cpu]))
                raise CPUFreqBaseError(("ERROR: Frequency should be lt max "
                                        "freq: {}".format(max_freqs[cpu])))
        return True

    def set_governors(self, gov, rg=None):
        """
        Set governors

        gov: str name of the governor
        rg: list of range of cores
        """
        to_change = self.__get_ranges("online")
        if isinstance(rg, int):
            rg = [rg]
        if rg:
            to_change = set(rg) & set(self.__get_ranges("online"))
        for cpu in to_change:
            fpath = path.join("cpu%i" % cpu, "cpufreq", "scaling_governor")
            self.__write_cpu_file(fpath, gov.encode())
        return True

    def get_online_cpus(self):
        """
        Get current online cpus
        """
        return self.__get_ranges("online")

    def get_governors(self):
        """
        Get current governors
        """
        return self.__get_cpu_variable("scaling_governor")

    def get_frequencies(self):
        """
        Get current frequency speed
        """
        freqs = self.__get_cpu_variable("scaling_cur_freq")
        for i in freqs:
            freqs[i] = int(freqs[i])
        return freqs
    
    def get_available_frequencies(self):
        """
        Get available frequencies
        """
        return self.available_frequencies
    
    def get_available_governors(self):
        """
        Get available governors
        """
        return self.available_governors
    
    def get_driver(self):
        """
        Get driver
        """
        return self.driver

    def get_max_freq(self, rg=None):
        """
        Get max frequency possible

        rg: list of range of cores
        """
        to_load = self.__get_ranges("online")
        if isinstance(rg, int):
            rg = [rg]
        if rg:
            to_load = set(rg) & set(self.__get_ranges("online"))
        data = {}
        for cpu in to_load:
            fpath = path.join("cpu%i" % cpu, "cpufreq", "scaling_max_freq")
            data[int(cpu)] = int(self.__read_cpu_file(
                fpath).rstrip("\n").split()[0])
        return data

    def get_min_freq(self, rg=None):
        """
        Get min frequency possible
        rg: list of range of cores
        """
        to_load = self.__get_ranges("online")
        if isinstance(rg, int):
            rg = [rg]
        if rg:
            to_load = set(rg) & set(self.__get_ranges("online"))
        data = {}
        for cpu in to_load:
            fpath = path.join("cpu%i" % cpu, "cpufreq", "scaling_min_freq")
            data[int(cpu)] = int(self.__read_cpu_file(
                fpath).rstrip("\n").split()[0])
        return data
    
    def run(self):
        while True:
            conn, addr = self.sock.accept()
            data = conn.recv(4096)

            order = yaml.load(data)
            # print(data)
            print(order)
            ret = 0

            if order['name'] == 'enable_all_cpu':
                ret = self.enable_all_cpu()
            elif order['name'] == 'reset':
                ret = self.reset()
            elif order['name'] == 'disable_hyperthread':
                ret = self.disable_hyperthread()
            elif order['name'] == 'disable_cpu':
                ret = self.disable_cpu(order['rg'])
                # print(ret)
            elif order['name'] == 'enable_cpu':
                ret = self.enable_cpu(order['rg'])
            elif order['name'] == 'set_frequencies':
                ret = self.set_frequencies(order['freq'], order['rg'])
            elif order['name'] == 'set_min_frequencies':
                ret = self.set_min_frequencies(order['minfreq'], order['rg'])
            elif order['name'] == 'set_max_frequencies':
                ret = self.set_max_frequencies(order['maxfreq'], order['rg'])
            elif order['name'] == 'set_governors':
                ret = self.set_governors(order['gover'], order['rg'])
            elif order['name'] == 'get_online_cpus':
                ret = self.get_online_cpus()
            elif order['name'] == 'get_governors':
                ret = self.get_governors()
            elif order['name'] == 'get_frequencies':
                ret = self.get_frequencies()
            elif order['name'] == 'get_available_governors':
                ret = self.get_available_governors()
            elif order['name'] == 'get_available_frequencies':
                ret = self.get_available_frequencies()
            elif order['name'] == 'get_driver':
                ret = self.get_driver()
            
            elif order['name'] == 'shutdown':
                conn.send(str.encode("0"))
                conn.close()
                print("[cpufreq_manager.py] Shutdown process manager")
                break
            else:
                print("Error: unknown operation key: '{}'".format(order['name']))
                ret = -1
            if ret:
                conn.send(str.encode(str(ret)))
            else:
                st = time.time() # for *debug*
                #dat = yaml.dump(ret) ## too slow!
                dat = pickle.dumps(ret)
                tt = time.time() - st # for *debug*
                print("** dump", tt, "sec")
                slen = 0
                try:
                    while slen < len(dat):
                        slen += conn.send(dat[slen:])
                except socket.error:
                    print('socket failed')
                tt = time.time() - st # for *debug*
                print("** sent", tt, "sec, size", len(dat))
                #print "** md5", hashlib.md5(dat).hexdigest()
                conn.close()

if __name__ == "__main__":
    if os.getuid() != 0:
        print("You must run runtime manger as root user")
        sys.exit(-1)

    # drop_capabilities()
    cpu = cpuFreq()
    cpu.run()
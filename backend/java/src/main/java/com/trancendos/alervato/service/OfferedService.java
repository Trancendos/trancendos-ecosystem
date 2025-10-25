package com.trancendos.alervato.service;

import com.trancendos.alervato.model.CustomerService;
import com.trancendos.alervato.repository.CustomerServiceRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class OfferedService {

    @Autowired
    private CustomerServiceRepository customerServiceRepository;

    public List<CustomerService> findAll() {
        return customerServiceRepository.findAll();
    }

    public CustomerService save(CustomerService customerService) {
        return customerServiceRepository.save(customerService);
    }
}
